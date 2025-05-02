import argparse
import datetime
import os
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET

from xml.dom import minidom

ns = 'http://schemas.microsoft.com/windows/2004/02/mit/task'

class NSElementMaker:
    """
    Automatically add namespace to elements.
    """

    def __init__(self, namespace):
        self.namespace = namespace

    def __call__(self, tag, text=None, attrib=None):
        el = ET.Element(f'{{{self.namespace}}}{tag}', attrib or {})
        if text:
            el.text = text
        return el


class SchtasksXML:
    """
    Create XML element trees for creating scheduled tasks.
    """

    def __init__(self, element_maker):
        self.E = element_maker

    def trigger_every_minutes(
        self,
        interval_minutes,
        start_boundary = None
    ):
        calendar = self.E('CalendarTrigger')

        repetition = self.E('Repetition')
        repetition.append(self.E('Interval', text=f'PT{interval_minutes}M'))
        repetition.append(self.E('Duration', text='P1D'))
        repetition.append(self.E('StopAtDurationEnd', text='false'))
        calendar.append(repetition)

        if start_boundary is None:
            start_boundary = midnight()
        calendar.append(self.E('StartBoundary', text=start_boundary.strftime('%Y-%m-%dT%H:%M:%S')))

        calendar.append(self.E('Enabled', text='true'))
        schedule_by_day = self.E('ScheduleByDay')
        schedule_by_day.append(self.E('DaysInterval', text='1'))
        calendar.append(schedule_by_day)

        return calendar

    def create_task_xml(
        self,
        task_name,
        script_path,
        python_path,
        interval_minutes,
        working_dir = None,
        description = None,
        trigger_type = 'Logon',
    ):
        ET.register_namespace('', ns)
        E = NSElementMaker(namespace=ns)

        task = self.E('Task', attrib={'version': '1.2'})

        registration_info = self.E('RegistrationInfo')
        if description:
            registration_info.append(self.E('Description', text=description))
        task.append(registration_info)

        triggers = self.E('Triggers')
        calendar = self.trigger_every_minutes(interval_minutes)
        triggers.append(calendar)
        task.append(triggers)

        settings = self.E('Settings')
        settings.append(self.E('MultipleInstancesPolicy', 'IgnoreNew'))
        settings.append(self.E('StartWhenAvailable', 'true'))
        settings.append(self.E('Enabled', 'true'))
        settings.append(self.E('Hidden', 'false'))
        settings.append(self.E('ExecutionTimeLimit', 'PT0S'))
        task.append(settings)

        actions = self.E('Actions', attrib={'Context': 'Author'})
        exec_elem = self.E('Exec')
        exec_elem.append(self.E('Command', python_path))
        exec_elem.append(self.E('Arguments', script_path))
        if working_dir:
            exec_elem.append(self.E('WorkingDirectory', working_dir))
        actions.append(exec_elem)
        task.append(actions)

        return ET.ElementTree(task)


def midnight(date=None):
    """
    Return date at midnight, defaulting to today.
    """
    if date is None:
        date = datetime.date.today()
    return datetime.datetime.combine(date, datetime.time())

def run(cmd, **kwargs):
    """
    Convenience for running commands silently.
    """
    kwargs.setdefault('check', True)
    kwargs.setdefault('capture_output', True)
    return subprocess.run(cmd, **kwargs)

def task_exists(task_name):
    """
    Return if a task name exists.
    """
    cmd = ['schtasks', '/query', '/tn', task_name]
    try:
       run(cmd)
       return True
    except subprocess.CalledProcessError:
       return False

def delete_task(task_name):
    return run(['schtasks', '/delete', '/tn', task_name, '/f'])

def pretty_xml(element_tree):
    rough_string = ET.tostring(element_tree.getroot(), 'utf-8')
    parsed = minidom.parseString(rough_string)
    return parsed.toprettyxml(indent='    ')

def register_task(
    task_name,
    script_path,
    python_path,
    interval_minutes,
    working_dir = None,
    description = None,
    remove_exists = False,
):
    """
    Create scheduled task to run every N minutes.
    """
    schtaskxml = SchtasksXML(NSElementMaker(ns))
    xml_tree = schtaskxml.create_task_xml(
        task_name,
        script_path,
        python_path,
        interval_minutes,
        working_dir = working_dir,
        description = description,
    )

    # Write XML to temporary file without deleting.
    with tempfile.NamedTemporaryFile(delete=False, suffix='.xml') as xml_file:
        xml_tree.write(xml_file, encoding='utf-16', xml_declaration=True)
        temp_xml_path = xml_file.name

    # Build subprocess command.
    cmd = ['schtasks', '/create', '/TN', task_name, '/XML', temp_xml_path]

    # Create scheduled task, removing if exists and configured to do so.
    # Finally, remove temporary file.
    try:
        if task_exists(task_name):
            if not remove_exists:
                raise ValueError('Task already exists.')
            delete_task(task_name)
        run(cmd)
    finally:
        os.remove(temp_xml_path)
