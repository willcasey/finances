import mintapi


mint = mintapi.Mint(
'wcasey17@gmail.com',  # Email used to log in to Mint
'Sand45top%',  # Your password used to log in to mint
# Optional parameters
mfa_method='sms',  # Can be 'sms' (default), 'email', or 'soft-token'.
                   # if mintapi detects an MFA request, it will trigger the requested method
                   # and prompt on the command line.
headless=True,  # Whether the chromedriver should work without opening a
                 # visible window (useful for server-side deployments)
mfa_input_callback=None,  # A callback accepting a single argument (the prompt)
                          # which returns the user-inputted 2FA code. By default
                          # the default Python `input` function is used.
session_path=None, # Directory that the Chrome persistent session will be written/read from.
                   # To avoid the 2FA code being asked for multiple times, you can either set
                   # this parameter or log in by hand in Chrome under the same user this runs
                   # as.
imap_account=None, # account name used to log in to your IMAP server
imap_password=None, # account password used to log in to your IMAP server
imap_server=None,  # IMAP server host name
imap_folder='INBOX',  # IMAP folder that receives MFA email
wait_for_sync=False,  # do not wait for accounts to sync
wait_for_sync_timeout=300,  # number of seconds to wait for sync
)
