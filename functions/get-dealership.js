const Cloudant = require('@cloudant/cloudant');

function main(params) {
    const cloudant = Cloudant({
        url: params.COUCH_URL,
        plugins: { iamauth: { iamApiKey: params.IAM_API_KEY } }
    });

    // Access your database (change 'mydatabase' to your actual database name)
    const db = cloudant.db.use('dealerships');

    if (!params.state) {
        return { error: "State parameter is required." };
    }

    // Query the database for dealerships in the specified state
    return db.list({ include_docs: true })
        .then((body) => {
            const dealerships = body.rows.map((row) => row.doc);
            const stateDealerships = dealerships.filter((dealership) => dealership.state === params.state);
            if (stateDealerships.length > 0) {
                return { dealerships: stateDealerships };
            } else {
                return { error: "No dealerships found for the specified state." };
            }
        })
        .catch((error) => {
            return { error: error.description };
        });
}
