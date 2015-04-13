# TODO: move this code to the bitcoin payment module.
def check_completion(activity):
    amount = activity.get_total_pledge_amount()

    if amount >= activity.goal and not activity.completed:
        # set the activity to completed so no one else can pledge.
        activity.completed = True
        activity.save()
        s = None
        # s = jsonrpclib.Server(get_rpc_address())
        s.sendtoaddress(activity.target_account.btc_address, float(activity.goal),
            'buy-uk-a-beer')
