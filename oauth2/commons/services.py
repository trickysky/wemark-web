from oauth2.models import UserRole

from collections import defaultdict
import logging


class AuthorizationService(object):
    DEFAULT_RESOURCE_OPERATION_SEPARATOR = ':'

    @staticmethod
    def get_permissions_by_role_name(role_name):
        ret = defaultdict(list)
        try:
            role = UserRole.objects.get(name=role_name)
            for permission in role.permissions:
                ret[permission.resource.name].append(permission.operation.name)
        except UserRole.DoesNotExist:
            logging.error('UserRole matching query does not exist')
        return ret

    @staticmethod
    def parse_permission(permission):
        """
        :type permission: str
        """
        ro = permission.split(AuthorizationService.DEFAULT_RESOURCE_OPERATION_SEPARATOR)
        return ro[0], ro[1] if len(ro) == 2 else None
