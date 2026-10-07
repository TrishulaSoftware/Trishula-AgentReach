from reach_engine import SovereignAgentReach

reach = SovereignAgentReach()

def snipe_x(url: str):
    return reach.inspect_x_post(url)

def snipe_reddit(url: str):
    return reach.inspect_reddit_post(url)
