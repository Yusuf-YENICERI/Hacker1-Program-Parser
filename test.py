from asyncore import write
import requests
import csv


def write_to_csv(programs):
  program = programs[0]
  program_keys = list(program.keys())
  program_keys.pop(2)
  program_keys.pop(2)
  program_keys += ["attributes_" + key for key in list(program['attributes'].keys())]

  program_keys += ["scopes_" + key for key in list(program['relationships']['structured_scopes']['data'][0].keys()) if key != "attributes"]
  program_keys += ["scopes_attributes_" + key for key in list(program['relationships']['structured_scopes']['data'][0]['attributes'].keys())]
  
  with open('results.csv', 'w') as file:
    writer = csv.writer(file)

    writer.writerow(program_keys)

    for program in programs:
      program_values = list(program.values())
      program_values.pop(2)
      program_values.pop(2)
      program_values += list(program['attributes'].values())
      
      for scope in list(program['relationships']['structured_scopes']['data']):
        temp_program_values = program_values.copy()  
        temp_program_values += list(scope.values())
        temp_program_values.pop(len(temp_program_values)-1)
        temp_program_values += list(scope['attributes'].values())

        writer.writerow(temp_program_values)

programs = []
counter = 2

headers = {
  'Accept': 'application/json'
}

r = requests.get(
  'https://api.hackerone.com/v1/hackers/programs?page[number]=1',
  auth=('nick', 'api-key'),
  headers = headers
)
extra_counter = 1
while True:

    for program in r.json()['data']:
        if (program['attributes']['state'] == 'public_mode') and (program['attributes']['offers_bounties'] == True):
            program_request = requests.get(
            'https://api.hackerone.com/v1/hackers/programs/' + program['attributes']['handle'],
            auth=('nick', 'api-key'),
            headers = headers
            )
            _program = program_request.json()
            programs.append(_program)
            print(_program)
            extra_counter += 1
            if extra_counter == 10:
              break


    break

    r = requests.get(
        'https://api.hackerone.com/v1/hackers/programs?page[number]=' + str(counter),
        auth=('nick', 'api-key'),
        headers = headers
        )

    counter+=1


write_to_csv(programs)



