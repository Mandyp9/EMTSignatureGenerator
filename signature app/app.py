from flask import Flask, render_template, request
import hashlib

app = Flask(__name__)

# API field configurations
api_fields = {
    "Choose the API": [],
    "Send Transaction": [
        "AGENT_CODE", "USER_ID", "AGENT_SESSION_ID", "AGENT_TXNID", "LOCATION_ID",
        "SENDER_FIRST_NAME", "SENDER_MIDDLE_NAME", "SENDER_LAST_NAME", "SENDER_GENDER",
        "SENDER_ADDRESS", "SENDER_CITY", "SENDER_COUNTRY", "SENDER_ID_TYPE",
        "SENDER_ID_NUMBER", "SENDER_ID_ISSUE_DATE", "SENDER_ID_EXPIRE_DATE",
        "SENDER_DATE_OF_BIRTH", "SENDER_MOBILE", "SOURCE_OF_FUND", "SENDER_OCCUPATION",
        "SENDER_NATIONALITY", "RECEIVER_FIRST_NAME", "RECEIVER_MIDDLE_NAME",
        "RECEIVER_LAST_NAME", "RECEIVER_ADDRESS", "RECEIVER_CITY", "RECEIVER_COUNTRY",
        "RECEIVER_CONTACT_NUMBER", "RELATIONSHIP_TO_BENEFICIARY", "PAYMENT_MODE",
        "BANK_ID", "BANK_NAME", "BANK_BRANCH_NAME", "BANK_ACCOUNT_NUMBER", "WALLET_ID",
        "CALC_BY", "TRANSFER_AMOUNT", "OURSERVICE_CHARGE", "TRANSACTION_EXCHANGERATE",
        "SETTLEMENT_DOLLARRATE", "PURPOSE_OF_REMITTANCE", "ADDITIONAL_FIELD1",
        "ADDITIONAL_FIELD2", "AUTHORIZED_REQUIRED", "API_PASSWORD"
    ],
    "Account Validation": [
        "AGENT_CODE", "USER_ID", "AGENT_SESSION_ID", "PAYMENT_MODE", "BankCode",
        "AccountNumber", "AccountName", "API_PASSWORD"
    ],
    "Get Exchange Rate": [
        "AGENT_CODE", "USER_ID", "AGENT_SESSION_ID", "TRANSFER_AMOUNT", "PAYMENT_MODE",
        "CALC_BY", "LOCATION_ID", "PAYOUT_COUNTRY", "API_PASSWORD"
    ],
    "SSF Validation": [
        "AGENT_CODE", "USER_ID", "AGENT_SESSION_ID", "PAYMENT_MODE", "BankCode",
        "PSSID", "API_PASSWORD"
    ],
    "Wallet Validation": [
        "AGENT_CODE", "USER_ID", "AGENT_SESSION_ID", "WalletId", "AccountName",
        "TransferAmount", "API_PASSWORD"
    ],
    "Fonepay Validation": [
        "AGENT_CODE", "USER_ID", "AGENT_SESSION_ID", "PAYMENT_MODE", "BankCode",
        "MobileNumber", "API_PASSWORD"
    ],
    "Ammendment Request": [
        "AGENT_CODE", "USER_ID", "AGENT_SESSION_ID", "PINNO", "AMENDMENT_FIELD",
        "AMENDMENT_VALUE", "API_PASSWORD"
    ],
    "Authorized Confirmed": [
        "AGENT_CODE", "USER_ID", "PINNO", "AGENT_SESSION_ID", "API_PASSWORD"
    ],
    "Cancel Transaction": [
        "AGENT_CODE", "USER_ID", "PINNO", "AGENT_SESSION_ID", "CANCEL_REASON",
        "API_PASSWORD"
    ],
    "Get Current Balance": [
        "AGENT_CODE", "USER_ID", "AGENT_SESSION_ID", "API_PASSWORD"
    ],
    "Query Txn Status": [
        "AGENT_CODE", "USER_ID", "PINNO", "AGENT_SESSION_ID", "AGENT_TXNID",
        "API_PASSWORD"
    ]
}


@app.route("/", methods=["GET", "POST"])
def index():
    selected_api = request.form.get("api") if request.method == "POST" else None
    fields = api_fields.get(selected_api, []) if selected_api else []
    values = {}
    signature = None
    concatenated = None

    if request.method == "POST" and selected_api and fields:
        # Collect field values
        for field in fields:
            values[field] = request.form.get(field, "")

        # Only generate SHA-256 if at least one field has a value
        if any(values.values()):
            # Concatenate values in the exact field order
            concatenated = "".join([values[field] for field in fields])

            # Generate SHA-256 hash
            signature = hashlib.sha256(concatenated.encode()).hexdigest()

    return render_template(
        "index.html",
        api_fields=api_fields,
        selected_api=selected_api,
        fields=fields,
        values=values,
        concatenated=concatenated,
        signature=signature
    )


# if __name__ == "__main__":
#     app.run(debug=True)
