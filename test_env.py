import requests, json

BASE = 'http://localhost:8000'

# 1. Health
h = requests.get(f'{BASE}/health').json()
print('HEALTH:', h)

# 2. Reset - all 3 tasks
for task in ['priority-triage', 'full-routing', 'full-pipeline']:
    r = requests.post(f'{BASE}/reset', json={'task': task, 'seed': 42}).json()
    obs = r['observation']
    print(f'\nRESET [{task}]: total_emails={r["total_emails"]} email_id={obs["email_id"]} subject={repr(obs["subject"][:50])}')

# 3. Step (on full-pipeline which was last reset)
step_r = requests.post(f'{BASE}/step', json={
    'priority': 'urgent',
    'category': 'technical',
    'reply_draft': 'We will investigate this immediately and escalate to our on-call team.'
}).json()
print(f'\nSTEP: reward={step_r["reward"]} done={step_r["done"]}')
print('  breakdown:', step_r['reward_breakdown'])
print('  ground_truth:', step_r.get('info', {}).get('ground_truth'))

# 4. State
state = requests.get(f'{BASE}/state').json()
print(f'\nSTATE: step={state["step_number"]} emails_done={state["emails_done"]} episode_reward={state["episode_reward"]}')

# 5. Tasks list
tasks = requests.get(f'{BASE}/tasks').json()
print(f'\nTASKS: {[t["name"] for t in tasks["tasks"]]}')

# 6. Verify graders directly
import sys
sys.path.insert(0, '.')
from server.graders import grade_priority, grade_category, grade_reply
print(f'\nGRADER TESTS:')
print(f'  grade_priority urgent==urgent: {grade_priority("urgent","urgent")}   (expect 1.0)')
print(f'  grade_priority high==urgent:   {grade_priority("high","urgent")}   (expect 0.5)')
print(f'  grade_priority low==urgent:    {grade_priority("low","urgent")}   (expect 0.0)')
print(f'  grade_category billing==billing: {grade_category("billing","billing")}  (expect 1.0)')
print(f'  grade_category general==billing: {grade_category("general","billing")} (expect 0.0)')
print(f'  grade_reply with keywords: {grade_reply("We will escalate and investigate the error", ["escalate","investigate","team"])}')
print('\nAll checks passed!')
