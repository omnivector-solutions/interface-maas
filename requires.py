from charms.reactive import when, when_not
from charms.reactive import set_flag, clear_flag
from charms.reactive import Endpoint


class MAASRequires(Endpoint):

    @when('endpoint.{endpoint_name}.changed')
    def changed(self):
        if any(unit.received['secret'] for unit in self.all_joined_units):
            set_flag(self.expand_name('available'))

    @when_not('endpoint.{endpoint_name}.joined')
    def broken(self):
        clear_flag(self.expand_name('available'))

    def list_unit_data(self):
        """
        Returns a list of available HTTP services and their associated hosts
        and ports.
        The return value is a list of dicts of the following form::
            [
                {
                    'service_name': name_of_service,
                    'hosts': [
                        {
                            'secret': secret,
                            'maas_url': maas_url,
                        },
                        # ...
                    ],
                },
                # ...
            ]
        """
        units_data = []
        for relation in self.relations:
            for unit in relation.joined_units:
                secret = unit.received['secret']
                maas_url = unit.received['maas_url']
                if not (maas_url and secret):
                    continue
                units_data.append({
                    'secret': secret,
                    'maas_url': maas_url,
                })
        return units_data
