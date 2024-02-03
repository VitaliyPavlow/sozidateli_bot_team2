from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram_forms.forms import FormsManager
from core import settings

from .constants import (CONTACTS_INFO, DATE_FORMAT, DOCUMENTS_FOR_INTERVIEW,
                        GO_TO_INTERVIEW, GO_TO_MEETING, HELLO_COORDINATOR,
                        HELLO_MESSAGE, HELP_INFO, INFO_ABOUT_MEETING,
                        INTERVIEW_INVITATION, INTERVIEW_INVITATION_MESSAGE,
                        MEETING_INVITATION_MESSAGE, NO_MEETINGS_MESSAGE,
                        REFUSE_INTERVIEW, REFUSE_MEETING,
                        START_VOLUNTEERING_INFO)
from .forms import RegistrationForInterviewForm  # noqa
from .forms import RegistrationForMeetingForm  # noqa
from .functions import get_open_meetings
from .keyboards import get_invitation_keyboard

router = Router()


@router.message(CommandStart())
async def start(message: Message):
    if (message.from_user.id == int(settings.manager_chat_id)):
        return await message.answer(
            HELLO_COORDINATOR.format(full_name=message.from_user.full_name)
        )
    await message.answer(
        HELLO_MESSAGE.format(full_name=message.from_user.full_name)
    )
    await message.answer(START_VOLUNTEERING_INFO)

    open_meetings = await get_open_meetings()
    if len(open_meetings) > 0:
        await message.answer(
            MEETING_INVITATION_MESSAGE.format(
                date=open_meetings[0][1].strftime(DATE_FORMAT)
            ),
            reply_markup=get_invitation_keyboard(GO_TO_MEETING, REFUSE_MEETING)
        )
    else:
        await message.answer(NO_MEETINGS_MESSAGE)
        await show_interview_invitation(message)


@router.message(Command(commands=['go_to_open_meeting']))
async def registration_for_metting(
    message: Message, forms: FormsManager
) -> None:
    open_meetings = await get_open_meetings()
    if len(open_meetings) > 0:
        await message.answer(
            INFO_ABOUT_MEETING.format(
                date=open_meetings[0][1].strftime(DATE_FORMAT)
            )
        )
        await forms.show('registration-for-meeting-form')
    else:
        await message.answer(NO_MEETINGS_MESSAGE)
        await show_interview_invitation(message)


@router.message(F.text == GO_TO_MEETING)
async def show_metting_form(
    message: Message, forms: FormsManager
) -> None:
    await forms.show('registration-for-meeting-form')


@router.message(F.text == REFUSE_MEETING)
async def show_interview_invitation(message: Message) -> None:
    await message.answer(INTERVIEW_INVITATION)
    await message.answer(
        INTERVIEW_INVITATION_MESSAGE,
        reply_markup=get_invitation_keyboard(
            GO_TO_INTERVIEW, REFUSE_INTERVIEW
        )
    )


@router.message(Command(commands=['go_to_interview']))
@router.message(F.text == GO_TO_INTERVIEW)
async def show_interview_form(
    message: Message, forms: FormsManager
) -> None:
    await forms.show('registration-for-interview-form')


@router.message(Command(commands=['help']))
@router.message(F.text == REFUSE_INTERVIEW)
async def command_help(message: Message) -> None:
    await message.answer(
        HELP_INFO,
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(Command(commands=['contacts']))
async def command_contacts(message: Message) -> None:
    await message.answer(CONTACTS_INFO)


@router.message(Command(commands=['documents']))
async def get_documents_list(message: Message) -> None:
    await message.answer(DOCUMENTS_FOR_INTERVIEW)


@router.message(Command(commands=['meeting_schedule']))
async def command_meeting_schedule(message: Message) -> None:
    open_meetings = await get_open_meetings()
    if len(open_meetings) > 0:
        for date in open_meetings:
            await message.answer(
                INFO_ABOUT_MEETING.format(
                    date=date[1].strftime(DATE_FORMAT)
                )
            )
        await message.answer(
            MEETING_INVITATION_MESSAGE.format(
                date=open_meetings[0][1].strftime(DATE_FORMAT)
            ),
            reply_markup=get_invitation_keyboard(
                GO_TO_MEETING, REFUSE_MEETING
            )
        )
    else:
        await message.answer(NO_MEETINGS_MESSAGE)
        await show_interview_invitation(message)
