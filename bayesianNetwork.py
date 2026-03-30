import pandas as pd
from pgmpy.models import DiscreteBayesianNetwork
from pgmpy.estimators import MaximumLikelihoodEstimator
from pgmpy.inference import VariableElimination

data = pd.DataFrame({
    'Rain': ['No', 'No', 'Yes', 'Yes', 'No', 'Yes', 'Yes', 'No'],
    'TrafficJam': ['Yes', 'No', 'Yes', 'No', 'Yes', 'Yes', 'No', 'No'],
    'ArriveLate': ['Yes', 'No', 'Yes', 'No', 'No', 'Yes', 'Yes', 'No']
})

model = DiscreteBayesianNetwork([
    ('Rain', 'TrafficJam'),
    ('TrafficJam', 'ArriveLate')
])

model.fit(data)

for cpd in model.get_cpds():
    print(cpd)

inference = VariableElimination(model)

result = inference.query(
    variables=['ArriveLate'],
    evidence={'Rain': 'Yes'}
)

print(result)