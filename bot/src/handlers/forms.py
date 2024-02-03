from aiogram.types import Message, ReplyKeyboardRemove
from aiogram_forms import dispatcher
from aiogram_forms.forms import Form, FormsManager, fields
from core import settings
from services import exceptions

from .constants import (INFO_ABOUT_USER_FOR_INTERVIEW,
                        INFO_ABOUT_USER_FOR_MEETING,
                        NAME_FIELD_TOO_SHORT_MESSAGE, SHOW_DOCUMENTS,
                        SUCCESS_FILL_INTERVIEW_FORM, SUCCESS_FILL_MEETING_FORM,
                        TRY_FILL_FORM_AGAIN, VOLUENTEERING_TYPE_QUESTION,
                        VOLUNTEERING_TYPE)
from .functions import register_user
from .validation import (validate_email_format, validate_phone_number_format,
                         validate_volunteering_type_field)


@dispatcher.register('registration-for-meeting-form')
class RegistrationForMeetingForm(Form):
    name = fields.TextField(
        'Ваше имя',
        min_length=2,
        error_messages={'min_length': NAME_FIELD_TOO_SHORT_MESSAGE}
    )
    phone = fields.PhoneNumberField(
        'Телефон',
        share_contact=True,
        validators=[validate_phone_number_format]
    )
    email = fields.EmailField('E-mail', validators=[validate_email_format])
    volunteering_type = fields.ChoiceField(
        VOLUENTEERING_TYPE_QUESTION,
        choices=VOLUNTEERING_TYPE,
        validators=[validate_volunteering_type_field]
    )

    @classmethod
    async def callback(
        cls, message: Message, forms: FormsManager, **data
    ) -> None:

        registration_data = await forms.get_data(
            'registration-for-meeting-form'
        )
        volunteering_type = ''.join(
            [item[0] for item in VOLUNTEERING_TYPE
                if registration_data['volunteering_type'] in item]
        )

        try:
            await register_user(
                name=registration_data['name'],
                phone=registration_data['phone'],
                email=registration_data['email'],
                assistance_segment=volunteering_type
            )
        except exceptions.HTTPRequestError as error:
            await message.answer(
                text=str(error),
                reply_markup=ReplyKeyboardRemove()
            )
            return await message.answer(
                text=TRY_FILL_FORM_AGAIN
            )

        await data['bot'].send_message(
            settings.manager_chat_id,
            INFO_ABOUT_USER_FOR_MEETING.format(
                username=data['event_from_user'].username,
                name=registration_data['name'],
                phone=registration_data['phone'],
                email=registration_data['email'],
                volunteering_type=volunteering_type
            )
        )
        await message.answer(
            text=SUCCESS_FILL_MEETING_FORM.format(
                name=registration_data['name']
            ),
            reply_markup=ReplyKeyboardRemove()
        )


@dispatcher.register('registration-for-interview-form')
class RegistrationForInterviewForm(Form):
    name = fields.TextField(
        'Ваше имя',
        min_length=2,
        error_messages={'min_length': NAME_FIELD_TOO_SHORT_MESSAGE}
    )
    phone = fields.PhoneNumberField(
        'Телефон',
        share_contact=True,
        validators=[validate_phone_number_format]
    )
    email = fields.EmailField('E-mail', validators=[validate_email_format])
    volunteering_type = fields.ChoiceField(
        VOLUENTEERING_TYPE_QUESTION,
        choices=VOLUNTEERING_TYPE,
        validators=[validate_volunteering_type_field]
    )

    @classmethod
    async def callback(
        cls, message: Message, forms: FormsManager, **data
    ) -> None:

        registration_data = await forms.get_data(
            'registration-for-interview-form'
        )
        volunteering_type = ''.join(
            [item[0] for item in VOLUNTEERING_TYPE
                if registration_data['volunteering_type'] in item]
        )

        await data['bot'].send_message(
            settings.manager_chat_id,
            INFO_ABOUT_USER_FOR_INTERVIEW.format(
                username=data['event_from_user'].username,
                name=registration_data['name'],
                phone=registration_data['phone'],
                email=registration_data['email'],
                volunteering_type=volunteering_type
            )
        )
        await message.answer(
            text=SUCCESS_FILL_INTERVIEW_FORM.format(
                name=registration_data['name']
            ),
            reply_markup=ReplyKeyboardRemove()
        )
        await message.answer(text=SHOW_DOCUMENTS)
