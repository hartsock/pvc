# Copyright (c) 2015 Marin Atanasov Nikolov <dnaeon@gmail.com>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer
#    in this position and unchanged.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR(S) ``AS IS'' AND ANY EXPRESS OR
# IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
# OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE AUTHOR(S) BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
# NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
# THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""
Datastore Widgets

"""

import humanize

import pvc.widget.alarm
import pvc.widget.common
import pvc.widget.event
import pvc.widget.menu
import pvc.widget.form
import pvc.widget.gauge
import pvc.widget.performance
import pvc.widget.virtualmachine

__all__ = ['DatastoreWidget', 'DatastoreActionWidget']


class DatastoreWidget(object):
    def __init__(self, agent, dialog, obj):
        """
        Datastore Widget

        Args:
            agent     (VConnector): A VConnector instance
            dialog (dialog.Dialog): A Dialog instance
            obj    (vim.Datastore): A Datastore managed entity

        """
        self.agent = agent
        self.dialog = dialog
        self.obj = obj
        self.title = '{} ({})'.format(self.obj.name, self.obj.__class__.__name__)
        self.display()

    def display(self):
        items = [
            pvc.widget.menu.MenuItem(
                tag='General',
                description='General information',
                on_select=self.info
            ),
            pvc.widget.menu.MenuItem(
                tag='Capacity',
                description='Datastore Capacity ',
                on_select=self.capacity
            ),
            pvc.widget.menu.MenuItem(
                tag='Actions',
                description='Available Actions',
                on_select=DatastoreActionWidget,
                on_select_args=(self.agent, self.dialog, self.obj)
            ),
            pvc.widget.menu.MenuItem(
                tag='Hosts',
                description='Hosts using the datastore',
                on_select=pvc.widget.common.hostmount_menu,
                on_select_args=(self.agent, self.dialog, self.obj)
            ),
            pvc.widget.menu.MenuItem(
                tag='Virtual Machines',
                description='Virtual Machines using the datastore',
                on_select=pvc.widget.common.virtual_machine_menu,
                on_select_args=(self.agent, self.dialog, self.obj)
            ),
            pvc.widget.menu.MenuItem(
                tag='Performance',
                description='Performance Metrics',
                on_select=pvc.widget.performance.PerformanceProviderWidget,
                on_select_args=(self.agent, self.dialog, self.obj)
            ),
            pvc.widget.menu.MenuItem(
                tag='Events',
                description='View Events',
                on_select=pvc.widget.event.EventWidget,
                on_select_args=(self.agent, self.dialog, self.obj)
            ),
            pvc.widget.menu.MenuItem(
                tag='Alarms',
                description='View triggered alarms',
                on_select=pvc.widget.common.alarm_menu,
                on_select_args=(self.agent, self.dialog, self.obj)
            ),
        ]

        menu = pvc.widget.menu.Menu(
            items=items,
            dialog=self.dialog,
            title=self.title,
            text='Select an action to be performed'
        )

        menu.display()

    def info(self):
        """
        Datastore general information

        """
        self.dialog.infobox(
            title=self.title,
            text='Retrieving information ...'
        )

        elements = [
            pvc.widget.form.FormElement(
                label='Name',
                item=self.obj.name,
            ),
            pvc.widget.form.FormElement(
                label='Location',
                item=self.obj.summary.url
            ),
            pvc.widget.form.FormElement(
                label='Type',
                item=self.obj.summary.type
            ),
            pvc.widget.form.FormElement(
                label='Accessible',
                item=str(self.obj.summary.accessible)
            ),
            pvc.widget.form.FormElement(
                label='Maintenance Mode',
                item=self.obj.summary.maintenanceMode
            ),
            pvc.widget.form.FormElement(
                label='Multiple Host Access',
                item=str(self.obj.summary.multipleHostAccess)
            ),
        ]

        form = pvc.widget.form.Form(
            dialog=self.dialog,
            form_elements=elements,
            title=self.title,
            text='Datastore general information'
        )

        form.display()

    def capacity(self):
        """
        Datastore Capacity Information

        """
        self.dialog.infobox(
            title=self.title,
            text='Retrieving information ...'
        )

        uncommitted = self.obj.summary.uncommitted if self.obj.summary.uncommitted else 0
        elements = [
            pvc.widget.form.FormElement(
                label='Capacity',
                item=humanize.naturalsize(self.obj.summary.capacity, binary=True)
            ),
            pvc.widget.form.FormElement(
                label='Free Space',
                item=humanize.naturalsize(self.obj.summary.freeSpace, binary=True)
            ),
            pvc.widget.form.FormElement(
                label='Uncommitted Space',
                item=humanize.naturalsize(uncommitted, binary=True)
            ),
        ]

        form = pvc.widget.form.Form(
            dialog=self.dialog,
            form_elements=elements,
            title=self.title,
            text='Datastore capacity information'
        )

        return form.display()


class DatastoreActionWidget(object):
    def __init__(self, agent, dialog, obj):
        """
        Datastore Actions Widget

        Args:
            agent     (VConnector): A VConnector instance
            dialog (dialog.Dialog): A Dialog instance
            obj    (vim.Datastore): A Datastore managed entity

        """
        self.agent = agent
        self.dialog = dialog
        self.obj = obj
        self.title = '{} ({})'.format(self.obj.name, self.obj.__class__.__name__)
        self.display()

    def display(self):
        items = [
            pvc.widget.menu.MenuItem(
                tag='Rename',
                description='Rename datastore',
                on_select=pvc.widget.common.rename,
                on_select_args=(self.obj, self.dialog)
            ),
            pvc.widget.menu.MenuItem(
                tag='Refresh',
                description='Refresh storage information',
                on_select=self.refresh
            ),
            pvc.widget.menu.MenuItem(
                tag='Remove',
                description='Remove datastore',
                on_select=pvc.widget.common.remove,
                on_select_args=(self.obj, self.dialog)
            ),
        ]

        menu = pvc.widget.menu.Menu(
            items=items,
            dialog=self.dialog,
            title=self.title,
            text='Select an action to be performed'
        )

        menu.display()

    def refresh(self):
        """
        Refresh storage related information

        """
        self.dialog.infobox(
            title=self.title,
            text='Refreshing storage information ...'
        )

        self.obj.RefreshDatastoreStorageInfo()
