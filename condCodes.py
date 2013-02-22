codes = {'Narwhal_SemPrime':('162', '163','164','165','166','167'), 'AUDI_random':('162', '163','164','165','166','167','168','169','170','171','172','173','174','178','179','180','181','182','183','184','185'),'Narwhal':('162','163','164','165','166','167','168','169','170','171','172','173','174','176','179','180','181','182','183','184'),'AUDI_blocked':('162','163','164','165','166','167','168','169','170','171','172','173','174','178','179','180','181','182','183','184','185'),'Narwhal':('162','163','164','165','166','167','168','169','170','171','172','173','174','176','179','180','181','182','183','184'),'f_m_pilot1_Run_1':('166','167','168','169','178','179','180','181'),'f_m_pilot2_Run_3':('166','167','168','169','178','179','180','181'),'m_f_pilot1_Run_2':('162','163','164','165','172','173','174','175'),'m_f_pilot2_Run_4':('162','163','164','165','172','173','174','175'),'onetone':('163')}

srates = {'Narwhal_SemPrime':500,'AUDI_random':1000,'AUDI_blocked':1000,'Narwhal':500,'f_m_pilot1_Run_1':1000,'f_m_pilot2_Run_3':1000,'m_f_pilot1_Run_2':1000,'m_f_pilot2_Run_4':1000,'onetone':500}

###These are specified in ms for convenience; conversion to samples happens below
preBase = {'Narwhal_SemPrime':200,'AUDI_random':100,'AUDI_blocked':100,'Narwhal':200,'f_m_pilot1_Run_1':100,'f_m_pilot2_Run_3':100,'m_f_pilot1_Run_2':100,'m_f_pilot2_Run_4':100,'onetone':100}
postBase = {'Narwhal_SemPrime':800,'AUDI_random':500,'AUDI_blocked':500,'Narwhal':1000,'f_m_pilot1_Run_1':500,'f_m_pilot2_Run_3':500,'m_f_pilot1_Run_2':500,'m_f_pilot2_Run_4':500,'onetone':500}



epochs = {}    ###This will be in samples

for exp in codes:
	count = 0
	temp = {}
	for code in codes[exp]:
		temp[codes[exp][count]] = [int(preBase[exp]*(float(srates[exp])/1000)),int(postBase[exp]*(float(srates[exp])/1000))]
		count = count + 1
	epochs[exp] = temp


condLabels = {'Narwhal_SemPrime': 
        	[['162','Related Targets'],
        	['163','Unrelated Targets'],
        	['164','Primes'],
        	['165','Animal Primes'],
        	['166','Animal Targets'],
        	['167','Post-animal Targets']],
        	'AUDI_random':
			[['162','Bark2'],
			['163','Bark3'],
			['164','Bark4'],
			['165','Bark5'],
			['166','Bark6'],
			['167','Bark7'],			
			['168','Bark8'],
			['169','Bark9'],
			['170','Bark10'],
			['171','Bark11'],
			['172','Bark12'],
			['173','Bark13'],
			['174','Bark14'],
			['178','Bark15'],
			['179','Bark16'],
			['180','Bark17'],
			['181','Bark18'],
			['182','Bark19'],
			['183','Bark20'],
			['184','Bark21']],
			'AUDI_blocked':
			[['162','Bark2'],
			['163','Bark3'],
			['164','Bark4'],
			['165','Bark5'],
			['166','Bark6'],
			['167','Bark7'],
			['168','Bark8'],
			['169','Bark9'],
			['170','Bark10'],
			['171','Bark11'],
			['172','Bark12'],
			['173','Bark13'],
			['174','Bark14'],
			['178','Bark15'],
			['179','Bark16'],
			['180','Bark17'],
			['181','Bark18'],
			['182','Bark19'],
			['183','Bark20'],
			['184','Bark21'],
			['185','Deviant']],
			'f_m_pilot1_Run_2':
			[['166','standard_f1'],
			['167','standard_f2'],
			['168','standard_f3'],
			['169','standard_f4'],
			['178','deviant_m1'],
			['179','deviant_m2'],
			['180','deviant_m3'],
			['181','deviant_m4']],
			'f_m_pilot2_Run_3':
			[['166','standard_f1'],
			['167','standard_f2'],
			['168','standard_f3'],
			['169','standard_f4'],
			['178','deviant_m1'],
			['179','deviant_m2'],
			['180','deviant_m3'],
			['181','deviant_m4']],
			'm_f_pilot1_Run_2':
			[['162','standard_m1'],
			['163','standard_m2'],
			['164','standard_m3'],
			['165','standard_m4'],
			['172','deviant_f1'],
			['173','deviant_f2'],
			['174','deviant_f3'],
			['175','deviant_f4']],
			'm_f_pilot2_Run_4':
			[['162','standard_m1'],
			['163','standard_m2'],
			['164','standard_m3'],
			['165','standard_m4'],
			['172','deviant_f1'],
			['173','deviant_f2'],
			['174','deviant_f3'],
			['175','deviant_f4']],
			'Narwhal': 
        	[['162','Neg ever'],
        	['166','Factive ever'],
        	['170','Ungram ever']],
        	'onetone':[['163','sound']]
			}