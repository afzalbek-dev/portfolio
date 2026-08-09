from aiogram.fsm.state import State, StatesGroup

class ProjectFSM(StatesGroup):
    category = State()
    title_uz = State()
    title_ru = State()
    title_en = State()
    desc_uz = State()
    desc_ru = State()
    desc_en = State()
    tech_stack = State()
    cover_image = State()
    screenshots = State()
    video_url = State()
    demo_url = State()
    bot_url = State()
    website_url = State()
    github_url = State()
    is_published = State()

class EditProjectFSM(StatesGroup):
    select_project = State()
    field_to_edit = State()
    new_value = State()

class VideoFSM(StatesGroup):
    title_uz = State()
    title_ru = State()
    title_en = State()
    desc_uz = State()
    desc_ru = State()
    desc_en = State()
    category = State()
    cover_image = State()
    video_file = State()
    tools = State()
    is_vertical = State()
    is_published = State()

class ServiceFSM(StatesGroup):
    slug = State()
    icon = State()
    title_uz = State()
    title_ru = State()
    title_en = State()
    desc_uz = State()
    desc_ru = State()
    desc_en = State()
    price = State()
    features_uz = State()
    features_ru = State()
    features_en = State()

class AboutFSM(StatesGroup):
    developer_name = State()
    developer_title = State()
    about_uz = State()
    about_ru = State()
    about_en = State()
    hero_title_uz = State()
    hero_title_ru = State()
    hero_title_en = State()
    hero_sub_uz = State()
    hero_sub_ru = State()
    hero_sub_en = State()

class ContactFSM(StatesGroup):
    select_key = State()
    edit_value = State()

class SettingFSM(StatesGroup):
    select_key = State()
    edit_value = State()

class AdminFSM(StatesGroup):
    add_admin_id = State()
    remove_admin_id = State()
