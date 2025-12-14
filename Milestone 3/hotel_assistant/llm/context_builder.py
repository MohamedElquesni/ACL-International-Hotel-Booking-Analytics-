"""Context Builder for LLM Prompts"""
from typing import Dict, Any

from typing import Dict, Any
import json

class ContextBuilder:
    """Builds optimized context for each intent type."""

    @staticmethod
    def build(intent: str, merged_data: Dict[str, Any]) -> str:
        """Route to intent-specific builder."""
        builders = {
            'LIST_HOTELS': ContextBuilder._build_list,
            'RECOMMEND_HOTEL': ContextBuilder._build_recommend,
            'DESCRIBE_HOTEL': ContextBuilder._build_describe,
            'COMPARE_HOTELS': ContextBuilder._build_compare,
            'CHECK_VISA': ContextBuilder._build_visa
        }

        builder = builders.get(intent, ContextBuilder._build_generic)
        return builder(merged_data)

    @staticmethod
    def _get_reviews_for_hotel(data: Dict[str, Any], hotel_name: str):
        """
        supporting_reviews might be:
        - dict: {hotel_name: [review_dicts]}
        - list: [review_dicts] (no hotel grouping)
        """
        sup = data.get("supporting_reviews")
        if not sup:
            return []

        if isinstance(sup, dict):
            return sup.get(hotel_name, []) or []

        if isinstance(sup, list):
            # If list of review dicts contains hotel_name field, filter it
            out = []
            for r in sup:
                if isinstance(r, dict) and r.get("hotel_name") == hotel_name:
                    out.append(r)
            return out

        return []

    @staticmethod
    def _build_list(data: Dict[str, Any]) -> str:
        if not data.get('metadata', {}).get('has_results'):
            return "No hotels found matching the criteria."

        context = "=== AVAILABLE HOTELS ===\n\n"
        for idx, hotel in enumerate(data.get('primary_results', []), 1):
            context += f"Hotel #{idx}\n"
            context += f"  Name: {hotel.get('hotel_name', 'N/A')}\n"
            context += f"  Location: {hotel.get('city_name', 'N/A')}, {hotel.get('country_name', 'N/A')}\n"
            context += f"  Star Rating: {hotel.get('star_rating', 'N/A')}/5\n"
            context += "\n"

        # Additional options from reviews (works whether supporting_reviews is list or dict)
        sup = data.get("supporting_reviews")
        extra = []
        if isinstance(sup, list):
            extra = sup[:5]
        elif isinstance(sup, dict):
            # pick 1 review per hotel up to 5 hotels
            for hname, reviews in list(sup.items())[:5]:
                if reviews:
                    extra.append(reviews[0] if isinstance(reviews, list) else {"hotel_name": hname})

        if extra:
            context += "=== ADDITIONAL OPTIONS FROM REVIEWS ===\n"
            for review in extra:
                context += f"  • {review.get('hotel_name', 'N/A')} in {review.get('city', review.get('city_name', 'N/A'))}\n"

        return context

    @staticmethod
    def _build_recommend(data: Dict[str, Any]) -> str:
        if not data.get('metadata', {}).get('has_results'):
            return "No recommendations available for this query."

        context = "=== HOTEL RECOMMENDATIONS ===\n\n"

        for idx, hotel in enumerate(data.get('primary_results', [])[:5], 1):
            hotel_name = hotel.get('hotel_name', 'Unknown')

            context += f"OPTION {idx}: {hotel_name}\n"
            context += f"Location: {hotel.get('city_name', 'N/A')}, {hotel.get('country_name', 'N/A')}\n\n"

            context += "SCORES:\n"
            if hotel.get('overall_review_score') is not None:
                context += f"  Overall: {float(hotel['overall_review_score']):.1f}/10\n"

            for aspect in ['cleanliness', 'comfort', 'facilities', 'location', 'staff', 'value_for_money']:
                key = f'{aspect}_review'
                if hotel.get(key) is not None:
                    context += f"  {aspect.replace('_', ' ').title()}: {float(hotel[key]):.1f}/10\n"

            if hotel.get('composite_aspect_score') is not None:
                context += f"  Composite Score: {float(hotel['composite_aspect_score']):.1f}/10\n"

            if hotel.get('review_count') is not None:
                context += f"  Based on: {hotel['review_count']} reviews\n"

            reviews = ContextBuilder._get_reviews_for_hotel(data, hotel_name)
            if reviews:
                context += "\nRECENT GUEST FEEDBACK:\n"
                for review in reviews[:2]:
                    traveller = review.get('traveller_type', 'Guest')
                    text = (review.get('review_text', '') or '')[:200]
                    context += f'  [{traveller}] "{text}..."\n'

            context += "\n" + "=" * 50 + "\n\n"

        return context

    @staticmethod
    def _build_describe(data: Dict[str, Any]) -> str:
        if not data.get('metadata', {}).get('has_results'):
            return "Hotel information not found."

        hotel = (data.get('primary_results') or [{}])[0]
        hotel_name = hotel.get('hotel_name', 'Unknown Hotel')

        context = f"=== {hotel_name.upper()} ===\n\n"
        context += f"Location: {hotel.get('city_name', 'N/A')}, {hotel.get('country_name', 'N/A')}\n\n"

        context += "HOTEL BASE STANDARDS:\n"
        for aspect in ['cleanliness', 'comfort', 'facilities', 'location', 'staff', 'value_for_money']:
            base_key = f'{aspect}_base'
            if hotel.get(base_key) is not None:
                context += f"  {aspect.replace('_', ' ').title()}: {hotel[base_key]}/10\n"

        context += "\nGUEST REVIEW SCORES:\n"
        for aspect in ['cleanliness', 'comfort', 'facilities', 'location', 'staff', 'value_for_money']:
            review_key = f'{aspect}_review'
            if hotel.get(review_key) is not None:
                context += f"  {aspect.replace('_', ' ').title()}: {float(hotel[review_key]):.1f}/10\n"

        if hotel.get('review_count') is not None:
            context += f"\nTotal Reviews: {hotel['review_count']}\n"

        reviews = ContextBuilder._get_reviews_for_hotel(data, hotel_name)
        if reviews:
            context += "\n=== GUEST EXPERIENCES ===\n\n"
            for idx, review in enumerate(reviews[:5], 1):
                traveller = review.get('traveller_type', 'Guest')
                text = review.get('review_text', '') or ''
                context += f"Review {idx} [{traveller}]:\n\"{text}\"\n\n"

        return context

    @staticmethod
    def _build_compare(data: Dict[str, Any]) -> str:
        if not data.get('metadata', {}).get('has_results'):
            return "Comparison data not available."

        comp = (data.get('primary_results') or [{}])[0]

        h1_name = comp.get('hotel1_name', 'Hotel 1')
        h2_name = comp.get('hotel2_name', 'Hotel 2')

        context = "=== HOTEL COMPARISON ===\n\n"
        context += f"HOTEL A: {h1_name}\n"
        context += f"Location: {comp.get('hotel1_city', 'N/A')}, {comp.get('hotel1_country', 'N/A')}\n\n"
        context += f"HOTEL B: {h2_name}\n"
        context += f"Location: {comp.get('hotel2_city', 'N/A')}, {comp.get('hotel2_country', 'N/A')}\n\n"

        context += "=== RATING COMPARISON (Base Standards) ===\n\n"
        context += f"{'Aspect':<20} | {h1_name[:15]:<15} | {h2_name[:15]:<15} | Difference\n"
        context += "-" * 75 + "\n"

        aspects = ['cleanliness', 'comfort', 'facilities', 'location', 'staff', 'value_for_money']
        for aspect in aspects:
            h1_key = f'hotel1_{aspect}_base'
            h2_key = f'hotel2_{aspect}_base'
            if comp.get(h1_key) is not None and comp.get(h2_key) is not None:
                h1_val = float(comp[h1_key])
                h2_val = float(comp[h2_key])
                diff = h1_val - h2_val
                diff_str = f"+{diff:.1f}" if diff > 0 else f"{diff:.1f}"
                aspect_name = aspect.replace('_', ' ').title()
                context += f"{aspect_name:<20} | {h1_val:>15.1f} | {h2_val:>15.1f} | {diff_str:>10}\n"

        # Add reviews if available
        sup = data.get("supporting_reviews")
        if sup:
            context += "\n=== GUEST REVIEWS ===\n\n"

            r1 = ContextBuilder._get_reviews_for_hotel(data, h1_name)
            if r1:
                context += f"--- {h1_name} ---\n"
                for review in r1[:2]:
                    context += f"[{review.get('traveller_type', 'Guest')}] {(review.get('review_text','') or '')[:150]}...\n\n"

            r2 = ContextBuilder._get_reviews_for_hotel(data, h2_name)
            if r2:
                context += f"--- {h2_name} ---\n"
                for review in r2[:2]:
                    context += f"[{review.get('traveller_type', 'Guest')}] {(review.get('review_text','') or '')[:150]}...\n\n"

        return context

    @staticmethod
    def _build_visa(data: Dict[str, Any]) -> str:
        if not data.get('metadata', {}).get('has_results'):
            return "Visa information not available."

        visa = (data.get('primary_results') or [{}])[0]

        context = "=== VISA REQUIREMENT ===\n\n"
        context += f"From Country: {visa.get('from_country', 'Unknown')}\n"
        context += f"To Country: {visa.get('to_country', 'Unknown')}\n"
        context += f"Visa Required: {'YES' if visa.get('visa_required') else 'NO'}\n"

        if visa.get('visa_type'):
            context += f"Visa Type: {visa['visa_type']}\n"

        return context

    @staticmethod
    def _build_generic(data: Dict[str, Any]) -> str:
        return json.dumps(data.get('primary_results', []), indent=2, ensure_ascii=False)


print("ContextBuilder class defined")
