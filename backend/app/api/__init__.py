from . import meetings, users, roles, administrations


routers = (users.router,
           meetings.router,
           roles.router,
           administrations.router)
