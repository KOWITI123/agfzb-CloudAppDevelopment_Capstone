from cloudant.client import Cloudant

def main(params):
    if 'review' in params:
        # Handle the POST request to post a review
        review = params['review']

        client = Cloudant.iam(
            account_name=params["COUCH_USERNAME"],
            api_key=params["IAM_API_KEY"],
            connect=True,
        )

        if not client:
            return { 'error': 'Failed to connect to the database.' }

        db = client['reviews']

        try:
            doc = db.create_document(review)
            return { 'message': 'Review posted successfully', 'id': doc['_id'] }
        except Exception as e:
            return { 'error': str(e) }
    elif 'dealerId' in params:
        # Handle the GET request to get reviews for a dealership
        client = Cloudant.iam(
            account_name=params["COUCH_USERNAME"],
            api_key=params["IAM_API_KEY"],
            connect=True,
        )

        if not client:
            return { 'error': 'Failed to connect to the database.' }

        db = client['reviews']

        result = db.get_query_result(
            selector={'dealership': int(params['dealerId'])},
            fields=['id', 'name', 'dealership', 'review', 'purchase', 'purchase_date', 'car_make', 'car_model', 'car_year']
        )

        reviews = [doc for doc in result]

        if reviews:
            return { 'reviews': reviews }
        else:
            return { 'error': 'No reviews found for the specified dealership.' }
    else:
        return { 'error': 'Invalid request. Use either GET with dealerId or POST with review data.' }
