#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r'''
---
module: my_own_module
short_description: Creates a text file on a remote host
description:
  - This module creates a text file on a remote host with specified content.
  - It can create directories recursively if they don't exist.
options:
  path:
    description:
      - The full path to the file to be created.
    required: true
    type: str
  content:
    description:
      - The content to write to the file.
    required: true
    type: str
  backup:
    description:
      - Create a backup of the original file before overwriting.
    required: false
    type: bool
    default: false
author:
  - Your Name (@ekwest93)
'''

EXAMPLES = r'''
- name: Create a file with content
  my_own_collection.my_own_module:
    path: /tmp/test.txt
    content: "Hello, World!"

- name: Create a file with backup
  my_own_collection.my_own_module:
    path: /etc/config.txt
    content: "config data"
    backup: true
'''

RETURN = r'''
path:
  description: Path to the file created.
  type: str
  returned: success
  sample: /tmp/test.txt
  changed:
  description: Whether the file was changed.
  type: bool
  returned: always
  sample: true
'''

import os
import shutil
from ansible.module_utils.basic import AnsibleModule

def run_module():
    module_args = dict(
        path=dict(type='str', required=True),
        content=dict(type='str', required=True),
        backup=dict(type='bool', required=False, default=False)
    )

    result = dict(
        changed=False,
        path='',
        message=''
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    path = module.params['path']
    content = module.params['content']
    backup = module.params['backup']

    # Проверяем, существует ли файл и не совпадает ли его содержимое
    file_exists = os.path.exists(path)
    file_content_matches = False

    if file_exists:
        with open(path, 'r') as f:
            existing_content = f.read()
            file_content_matches = (existing_content == content)

    if not file_exists or not file_content_matches:
        if module.check_mode:
            result['changed'] = True
            module.exit_json(**result)

        # Создаём резервную копию при необходимости
        if backup and file_exists:
            backup_path = path + '.backup'
            shutil.copy2(path, backup_path)
            result['backup_file'] = backup_path

        # Создаём директорию, если не существует
        directory = os.path.dirname(path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)

        # Записываем файл
        with open(path, 'w') as f:
            f.write(content)

        result['changed'] = True
        result['path'] = path
        result['message'] = "File created successfully"

    else:
        result['path'] = path
        result['message'] = "File already exists with correct content"

    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()
