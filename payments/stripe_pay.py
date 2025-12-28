import stripe
from config import STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY

def create_checkout_session(price_id: str, customer_email: str, success_url: str, cancel_url: str) -> str:
    """
    Create a Stripe checkout session for subscription payment.
    Returns a URL for the user to pay.
    """
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            mode="subscription",
            line_items=[{"price": price_id, "quantity": 1}],
            customer_email=customer_email,
            success_url=success_url + "?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=cancel_url,
        )
        return session.url
    except Exception as e:
        return f"Error creating checkout session: {str(e)}"
