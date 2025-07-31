import os
from dwollav2 import Client, Error
from typing import Optional
from app.core.config import settings


def extractCustomerIdFromUrl(url : str):
    #Split the URL string by '/'
    parts = url.split('/')
    
    #Extract the last part, which represents the customer ID
    customerId = parts[-1]

    return customerId

def get_environment() -> str:
    environment = settings.DWOLLA_ENV
    if environment in ["sandbox", "production"]:
        return environment
    raise ValueError("DWOLLA_ENV must be 'sandbox' or 'production'")


# Initialize Dwolla client
dwolla_client = Client(
    key = settings.DWOLLA_KEY,
    secret = settings.DWOLLA_SECRET,
    environment=get_environment()
)

import logging
from typing import Optional

logger = logging.getLogger(__name__)

# , type: str
async def create_dwolla_customer(new_customer: dict) -> Optional[str]:
    logger.info("create_dwolla_customer called")
    try:
        application_token = dwolla_client.Auth.client()
        res = dwolla_client.auth_url
        logger.info(f"Dwolla response: {res}")
        logger.info(f"res: {res}")
        logger.info(f"application_token: {application_token}")

        customer_response = application_token.post('customers', new_customer)
        customer_url = customer_response.headers['Location']
        logger.info(f"Customer created successfully: {customer_url}, type: {type(customer_url)}")
        
        return customer_url
    except Exception as e:
        print("Creating a Dwolla Customer Failed:", e)


def create_on_demand_authorization() -> Optional[dict]:
    try:
        response = dwolla_client.post("on-demand-authorizations")
        return response.body.get("_links")
    except Exception as e:
        print("Creating On Demand Authorization Failed:", e)


def create_funding_source(customer_id: str, funding_source_name: str, plaid_token: str) -> Optional[str]:
    try:
        res = dwolla_client.post(
            f"customers/{customer_id}/funding-sources",
            {
                "name": funding_source_name,
                "plaidToken": plaid_token
            }
        )
        return res.headers.get("location")
    except Exception as e:
        print("Creating Funding Source Failed:", e)


def create_transfer(
    source_funding_source_url: str,
    destination_funding_source_url: str,
    amount: str
) -> Optional[str]:
    try:
        request_body = {
            "_links": {
                "source": {"href": source_funding_source_url},
                "destination": {"href": destination_funding_source_url}
            },
            "amount": {
                "currency": "USD",
                "value": amount
            }
        }
        res = dwolla_client.post("transfers", request_body)
        return res.headers.get("location")
    except Exception as e:
        print("Transfer fund failed:", e)


def add_funding_source(
    dwolla_customer_id: str,
    processor_token: str,
    bank_name: str
) -> Optional[str]:
    try:
        dwolla_auth_links = create_on_demand_authorization()
        if not dwolla_auth_links:
            raise Exception("Authorization failed.")

        funding_source_url = create_funding_source(
            customer_id=dwolla_customer_id,
            funding_source_name=bank_name,
            plaid_token=processor_token
        )
        return funding_source_url
    except Exception as e:
        print("Add Funding Source Failed:", e)
