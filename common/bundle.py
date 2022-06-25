
from zipline.data.bundles import register
from zipline.data.bundles.csvdir import csvdir_equities
register(
    'custom-csvdir-bundle',
    csvdir_equities(
        ['daily'],
        '/home/ubuntu/Downloads/nifty_10min_data.csv',
    ),
    calendar_name='nifty', # US equities
    #start_session=start_session,
    #end_session=end_session
)