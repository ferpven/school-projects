
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

diff = ctrl.Antecedent(np.arange(0, 91, 1), 'piksel_farki')
yon = ctrl.Antecedent(np.arange(0,2,1),'yon')
acisal_hiz = ctrl.Consequent(np.linspace(0,0.9,num=500),'acisal_hiz')

diff['cok-yakin'] = fuzz.trimf(diff.universe, [0, 0, 30])
diff['yakin'] = fuzz.trimf(diff.universe, [15, 30, 45])
diff['orta'] = fuzz.trimf(diff.universe, [30, 45, 60])
diff['uzak'] = fuzz.trimf(diff.universe, [45, 60, 75])
diff['cok-uzak'] = fuzz.trimf(diff.universe, [60, 75, 90])
diff.view()

yon['sol']= fuzz.trimf(yon.universe,[0,0,1])
yon['sag']= fuzz.trimf(yon.universe,[0,1,2])
yon.view()

acisal_hiz['cok-sag'] = fuzz.trimf(acisal_hiz.universe, [0, 0, 0.3])
acisal_hiz['sag'] = fuzz.trimf(acisal_hiz.universe, [0.15, 0.3, 0.45])
acisal_hiz['duz'] = fuzz.trimf(acisal_hiz.universe, [0.3, 0.45, 0.6])
acisal_hiz['sol'] = fuzz.trimf(acisal_hiz.universe, [0.45, 0.6, 0.75])
acisal_hiz['cok-sol'] = fuzz.trimf(acisal_hiz.universe, [0.6, 0.75, 0.9])
acisal_hiz.view()


rule1 = ctrl.Rule(diff['cok-yakin'] & yon['sol'], acisal_hiz['sag'])
rule2 = ctrl.Rule(diff['cok-yakin'] & yon['sag'], acisal_hiz['sol'])

rule3 = ctrl.Rule(diff['yakin'] & yon['sol'], acisal_hiz['sag'])
rule4 = ctrl.Rule(diff['yakin'] & yon['sag'], acisal_hiz['sol'])

rule5 = ctrl.Rule(diff['orta'] & yon['sol'], acisal_hiz['duz'])
rule6 = ctrl.Rule(diff['orta'] & yon['sag'], acisal_hiz['duz'])

rule7 = ctrl.Rule(diff['uzak'] & yon['sol'], acisal_hiz['sag'])
rule8 = ctrl.Rule(diff['uzak'] & yon['sag'], acisal_hiz['sol'])

rule9 = ctrl.Rule(diff['cok-uzak'] & yon['sol'], acisal_hiz['cok-sag'])
rule10 = ctrl.Rule(diff['cok-uzak'] & yon['sag'], acisal_hiz['cok-sol'])


acisal_hiz_ctrl = ctrl.ControlSystem([rule1,rule2,rule3,rule4,rule5,rule6,rule7,rule8,rule9,rule10])

acisal_hiz_out = ctrl.ControlSystemSimulation(acisal_hiz_ctrl)
acisal_hiz_out.input['piksel_farki'] = 10
acisal_hiz_out.input['yon']= 0

acisal_hiz_out.compute()
print(acisal_hiz_out.output['acisal_hiz']-0.5)
acisal_hiz.view(sim=acisal_hiz_out)

input('Press any key to exit!')