#!/usr/bin/python
from ansible.module_utils.basic import AnsibleModule
import os

def run_module():
    module_args = dict(
        path=dict(type='str', required=True),
        content=dict(type='str', required=True)
    )
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)
    path = module.params['path']
    content = module.params['content']
    
    if os.path.exists(path):
        with open(path, 'r') as f:
            existing = f.read()
        if existing == content:
            module.exit_json(changed=False, path=path, message="File unchanged")
    
    if module.check_mode:
        module.exit_json(changed=True)
    
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(content)
    module.exit_json(changed=True, path=path, message="File created")

def main():
    run_module()

if __name__ == '__main__':
    main()
