import re


class NamesRolesProvisioningService(object):
    _service_connector = None
    _service_data = None

    def __init__(self, service_connector, service_data):
        self._service_connector = service_connector
        self._service_data = service_data

    def get_members(self):
        members = []
        next_page = self._service_data['context_memberships_url']

        while next_page:
            page = self._service_connector.make_service_request(
                ['https://purl.imsglobal.org/spec/lti-nrps/scope/contextmembership.readonly'],
                next_page,
                accept='application/vnd.ims.lti-nrps.v2.membershipcontainer+json'
            )

            members.extend(page.get('body', {}).get('members', []))

            next_page = False
            link_header = page.get('headers', {}).get('link', '')
            if link_header:
                match = re.search(r'<(.*)>; ?rel="next"', link_header.lower().strip())
                if match:
                    next_page = match.group(1)

        return members
