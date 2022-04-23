from os import system, path, environ

# Yaml (pyyaml)
from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader
import argparse

def get_config(config_file):
    global sourceDir
    with open(config_file, 'r') as f:
        config = load(f, Loader=Loader)
    sourceDir = config['global'].get('dotfiles', path.abspath(path.dirname(__file__)))
    return config

def full_path(strPath):
    return str(path.abspath(path.expanduser(path.expandvars(strPath))))


class File:
    def __init__(self, sourceDir, targetDir, yaml=''):
        if type(yaml) == str:
            self.path = full_path(path.join(sourceDir, yaml))
            self.targetPath = full_path(path.join(targetDir, yaml))
            self.toParse = False
        else:
            self.path = full_path(path.join(sourceDir, yaml['source']))
            self.targetPath = full_path(path.join(targetDir, yaml.get('source', yaml['source'])))
            self.toParse = yaml.get('parse', False)
        self.mkdir()

    def manage(self, variables):
        if self.toParse:
            return self.parse(variables)
        else:
            return self.link()

    def parse(self, variables):
        print(f'Parsing {self.path}')
        try:
            with open(self.path, 'r') as f:
                content = f.read()
            for key, value in variables.items():
                content = content.replace('%{{' + key + '}}', value)
            with open(self.targetPath, 'w') as f:
                f.write(content)
            return True
        except Exception as e:
            print(f'Error parsing {self.path}: {e}')
            return False

    def link(self):
        print(f'Linking {self.path}')
        res = system('ln -sfn ' + self.path + ' ' + self.targetPath)
        return (res == 0)

    def mkdir(self):
        dirName = path.dirname(self.targetPath)
        if not path.exists(dirName):
            print('Creating target directory %s' % dirName)
            res = system('mkdir -p %s' % dirName)
            return (res == 0)
        return True


class Module:
    def __init__(self, name, yaml):
        global sourceDir
        self.name = name
        self.enabled = yaml.get('enabled', True)
        self.dirname = yaml.get('dirname', name)
        self.packageName = yaml.get('packageName', None)
        self.dependencies = yaml.get('dependencies', [])
        self.targetPath = yaml.get('targetDir', '~/.config/' + self.dirname)
        self.files = yaml.get('files', [])
        self.customSteps = yaml.get('customSteps', [])
        self.sourcePath = sourceDir + '/' + self.dirname

    def install(self, config):
        if self.packageName:
            print('Installing module %s from package %s with dependencies %s' %
                    (self.name,
                    self.packageName,
                    ', '.join(self.dependencies)))
            if system(config['installCommand'] % self.packageName) == 0:
                for package in self.dependencies:
                    success = system(config['installCommand'] % package)
                    if success != 0:
                        print('Failed to install dependency %s' % package)
                        user = input('Continue anyway? (y/n) ')
                        if user != 'y':
                            return False
                return True
            else:
                print('Failed to install module %s, aborting' % self.name)
                return False

    def run_custom_steps(self):
        for step in self.customSteps:
            res = system(step)
            if res != 0:
                print('Failed to run custom step %s (return code %s), aborting' % (step, res))
                return False
        return True

    
    def link(self, variables):
        if self.files == []:
                return File(f'{self.sourcePath}/',
                        f'{self.targetPath}').link()
        for yaml in self.files:
            file = File(self.sourcePath, self.targetPath, yaml)
            if not file.manage(variables):
                return False
        return True

def config_path():
    for p in [environ.get('XDG_CONFIG_HOME', '~/.config'), '~']:
        if path.exists(full_path(p + '/ydots/config.yaml')):
            return full_path(p + '/ydots/config.yaml')
    return False

def main():
    parser = argparse.ArgumentParser(description='Install dotfiles')
    parser.add_argument('-c', help='Config file', required=(not config_path()))
    parser.add_argument('-i', help='Install packages')
    args = parser.parse_args()
    config_file = args.c or config_path()
    config = get_config(config_file)
    modules = [Module(name, config['modules'][name]) for name in config['modules']]
    for module in modules:
        if module.enabled:
            if not args.i or module.install(config['global']):
                if module.link(config['variables']):
                    if module.run_custom_steps():
                        print('Module %s successfully installed' % module.name)
                    

if __name__ == "__main__":
    main()
