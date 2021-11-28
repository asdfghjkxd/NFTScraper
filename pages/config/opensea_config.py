# change any of the parameters below to alter the default behaviour of the scraper
ACCOUNT_ADDRESS = None
API_KEY = None
ASSET_CONTRACT_ADDRESS = None
ASSET_CONTRACT_ADDRESSES = None
ASSET_OWNER = None
AUCTION_TYPE = None
COLLECTION = None
COLLECTION_SLUG = None
EVENT_TYPE = None
LIMIT = 20
OCCURRED_AFTER = None
OCCURRED_BEFORE = None
OFFSET = 0
ON_SALE = None
ONLY_OPENSEA = False
ORDER_BY = None
ORDER_DIRECTION = 'desc'
OWNER = None
TOKEN_ID = None
TOKEN_IDS = None

# change any of the following to modify the behavior of the app
RETRIEVAL_METHOD = 'Assets'
GET_ALL = False
ADVANCED = False
SAVE = True
VERBOSE = True
VERBOSITY = 20
QUERY_PARAMS = None
ASSERT_INPUTS = False
SAVED_OUTPUTS_ASSETS = ['name', 'description', 'external_link', 'asset_contract', 'permalink', 'collection', 'decimals',
                        'token_metadata', 'owner', 'sell_orders', 'creator', 'traits', 'last_sale', 'top_bid',
                        'listing_date', 'is_presale', 'transfer_fee_payment_token', 'transfer_fee']
SAVED_OUTPUTS_EVENTS = ['event_type', 'asset', 'asset_bundle', 'created_date', 'from_account', 'to_account',
                        'is_private', 'payment_token', 'quantity', 'total_price']
SAVED_OUTPUTS_COLLECTIONS = ['primary_asset_contracts', 'traits', 'stats', 'banner_image_url', 'chat_url',
                             'created_date', 'default_to_fiat', 'description', 'dev_buyer_fee_basis_points',
                             'dev_seller_fee_basis_points', 'discord_url', 'display_data', 'external_url', 'featured',
                             'featured_image_url', 'hidden', 'safelist_request_status', 'image_url',
                             'is_subject_to_whitelist', 'large_image_url', 'medium_username', 'name',
                             'only_proxied_transfers', 'opensea_buyer_fee_basis_points',
                             'opensea_seller_fee_basis_points', 'payout_address', 'require_email', 'short_description',
                             'slug', 'telegram_url', 'twitter_username', 'instagram_username', 'wiki_url']
SAVED_OUTPUTS_BUNDLES = ['maker', 'slug', 'assets', 'name', 'description', 'external_link', 'asset_contract',
                         'permalink', 'sell_orders']
SAVED_OUTPUTS_ACTUAL = []
