import yaml
from goldobot_ihm.hal_config import HALConfig
if __name__ == '__main__':
    path = 'PR_test_debut_2020'
    yaml = yaml.load(open(path + '/hal.yaml'),Loader=yaml.FullLoader)
    hal_config = HALConfig(yaml)
    print(hal_config.compile())
    