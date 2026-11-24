"""Local customer support policy and response knowledge base."""

KNOWLEDGE_BASE = {
    "delivery": {
        "context": (
            "Delivery policy: Customers should check their order status "
            "and tracking information. If an order is delayed, contact "
            "customer support with the order ID."
        ),
        "response": (
            "I understand your concern about the delivery. Please check "
            "your order tracking status. If the order is delayed, contact "
            "customer support with your order ID for further assistance."
        )
    },

    "refund": {
        "context": (
            "Refund policy: Refund eligibility depends on the order and "
            "the seller's return policy. Customers should submit a refund "
            "request with their order details."
        ),
        "response": (
            "I can help with your refund query. Please submit a refund "
            "request with your order ID and the reason for the request. "
            "The support team can then verify your eligibility."
        )
    },

    "payment": {
        "context": (
            "Payment policy: Customers should verify the transaction "
            "status. If money was deducted but the order was not confirmed, "
            "contact payment support with the transaction reference."
        ),
        "response": (
            "I understand your payment concern. Please check your bank "
            "transaction status. If money was deducted but the order was "
            "not confirmed, contact payment support with your transaction ID."
        )
    },

    "account": {
        "context": (
            "Account policy: Customers should use the official password "
            "reset process. Never share passwords or OTPs with anyone."
        ),
        "response": (
            "For account access issues, please use the official password "
            "reset option. Never share your password or OTP with anyone."
        )
    },

    "product": {
        "context": (
            "Product policy: Customers should provide the product name, "
            "order ID, and a description of the problem for investigation."
        ),
        "response": (
            "Please share the product name, order ID, and a description "
            "of the issue so the support team can investigate."
        )
    },

    "general": {
        "context": (
            "General support policy: Ask the customer for relevant details "
            "and direct them to the appropriate support team."
        ),
        "response": (
            "Thank you for contacting customer support. Please provide "
            "more details about your issue so we can assist you."
        )
    }
}


def classify_issue(message):
    """Classify a customer issue using simple keyword rules."""

    text = message.lower()

    if any(word in text for word in ["delivery", "delayed", "shipping", "tracking", "parcel"]):
        return "delivery"

    if any(word in text for word in ["refund", "return", "money back", "replacement"]):
        return "refund"

    if any(word in text for word in ["payment", "paid", "transaction", "deducted", "upi"]):
        return "payment"

    if any(word in text for word in ["login", "password", "account", "otp"]):
        return "account"

    if any(word in text for word in ["product", "damaged", "defective", "broken"]):
        return "product"

    return "general"


def retrieve_context(category):
    """Retrieve the matching support policy."""

    return KNOWLEDGE_BASE.get(category, KNOWLEDGE_BASE["general"])


def build_response(category):
    """Create a grounded response from the local knowledge base."""

    return retrieve_context(category)["response"]