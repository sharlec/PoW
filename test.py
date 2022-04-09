# %%
import client
# %%
outcome = client.buy_ticket("K98665")
if outcome is not False:
    print(f"succeed: {outcome}")
else:
    print("Failed")
# %%
