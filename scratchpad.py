import daos.exuberant_systems_dao as exuberant_systems_dao

exuberant_system = exuberant_systems_dao.get_single_exuberant_system('example_thesis', 'exuberant_systems')

print(len(exuberant_system.tournament))
