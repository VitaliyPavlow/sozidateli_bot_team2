from schemas import users as schema_user
from services import meetings, users

meeting_service = meetings.MeetingService()
user_service = users.UserService()


async def get_open_meetings():
    all_meetings = await meeting_service.get_meetings()
    open_meetings = []
    for meeting in all_meetings:
        if meeting.is_open:
            open_meetings.append((meeting.id, meeting.date))
    open_meetings.sort(key=lambda a: a[1])
    return open_meetings


async def register_user(name, phone, email, assistance_segment):
    meeting = await get_open_meetings()
    symbols = (' ', '(', ')', '+')
    for symbol in symbols:
        phone = phone.replace(symbol, '')
    phone = f'+{phone}'
    user = schema_user.UserCreate(
        name=name,
        phone=phone,
        email=email,
        meeting_id=meeting[0][0],
        assistance_segment=assistance_segment
    )

    await user_service.create_user(user)
