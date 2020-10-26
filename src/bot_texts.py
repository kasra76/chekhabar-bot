help_text = """شرایط کلی انتشار خبر:
منبع خبری:
هر خبر، باید به طور گویا نشان‌دهنده این مطلب باشه که از سمت چه شخصی (اسم واقعی یا مستعار)  منتشر شده. و همچنین تو توضیح اون باید مشخص شده باشه که این خبر مربوط به کجا و چه زمانیه.
حوزه‌های خبری:
اخبار ارسالی می‌تونن تو همه حوزه‌های خبری و مربوط به کل کشور باشن و از این لحاظ "چه خبر" محدودیتی ندارد.
قالب کلی خبر و مطلب ارسالی:
اخبار ارسالی از سوی مخاطبان به «چه خبر»، باید حاوی اطلاعات دقیق، متناسب با زمان، شفاف و دارای ارزش خبری و محتوایی و عاری از اغراق تبلیغاتی و درخواست مستقیم از مخاطب برای انجام کاری مرتبط با خرید محصولات و خدمات و به طور کلی، عاری از هرگونه پیام‌ هرزگونه باشد.
«چه خبر»، مختار است که اخبار دارای تاریخ قدیمی و فاقد زمان مشخص را منتشر نکند.
اخبار و محتوای مرتبط با فعالیت‌های غیرقانونی و یا فعالیت‌های هرزگونه از کانال «چه خبر» قابل انتشار و توزیع نیست."""


profileSetting_text = """:تنظیمات پروفایل
 در این قسمت شما می‌تونید تنظیمات پروفایل و مقدار امتیازات کسب شده خودتون رو مشاهده کنید."""


start_text = 'به بات چه خبر خوش آمدید . در اینجا شما گزارشگر خودتون هستید. گزارش‌هاتون رو مثل یک گزارشگر به بات ما بفرستید تا به نام خودتون یا نام مستعار توی کانال قرار بدیم.'


getContact_text = "برای شروع به شماره تماس شما نیاز داریم؛ به همین خاطر دکمه ارسال شماره را فشار دهید."


start_reporting = 'در این بخش شما می‌تونید گزارش خودتون رو برای ما ارسال کنید . برای شروع اول نام مستعار خودتون رو انتخاب کنید. برای انتخاب روی دکمه زیر کلیک کنید.'

getAliases_text = 'یکی از اسم های مستعار خود را که قبلا ثبت کرده اید را انتخاب کنید'

get_alias_while_reporting_text = "برای شما نام مستعاری ثبت نشده. برای ارسال گزارش ابتدا یک نام مستعار برای خود وارد کنید. دقت کنید که این نام مستعار جز نام های مستعار شما ثبت شده و قابل تغییر نمی‌باشد"

deny_text = 'حساب کاربری شما ساخته نشد. برای شروع دوباره بر روی /start کلیک کنید'

illigal_text = "ورودی نامعتبر است"

vegCleaning_text = """سبزی پاک کنیم!
منتظر یه چیز باحال باشید :)"""

regester_new_alias_text = "نام مستعار جدید خودتون رو وارد کنید. دقت کنید که بعد از ارسال نام مستعار، این نام مستعار برای شما ثبت شده و قابل تغییر نخواهد بود."

send_report_text = """ارسال گزارش
فرمت ارسال گزارش ها:
گزارش شما باید یکی از صورت های زیر باشد:
1- متن تنها
2- عکس + متن
3- ویدیو + متن
\U000026A0دقت کنید که فایل هارا به صورت جداگانه برای بات ارسال نکنید
"""

selected_alias_goto_city_text = """نام مستعار انتخاب شد در مرحله بعد
شهر مورد نظر خود را انتخاب کنید:
به این صورت که از لیست شهر ها زیر، شماره شهر مورد نظر را وارد کنیدو دقت کنید که حتما فقط شماره را بفرستید در غیر این صورت خطا نشان داده می شود
1 مشهد
2 تهران
3 اصفهان"""

city_selected_goto_report_text = "شهر مورد نظر انتخاب شد. برای شروع نوشتن گزارش ، دکمه نوشتن گزارش را بزنید"

get_add_new_alias_text = "نام مستعار جدید خود را وارد کنید. دقت کنید که بعد از ارسال نام مستعار ثبت شده و قابل تغییر نمی‌باشد"

tell_user_for_reject = '\U00002639	اووپس. ادمین گزارش شما رو قبول نکرد!'

tell_user_for_acc = """\U0001F389 ادمین گزارش شما رو قبول کرد
\U0001F39F شما یک سکه بدست آوردید"""

report_succ_sent = """
\U0001F389 گزارش شما با موفقیت ارسال شد
"""


def get_helpText():
    return help_text

def get_profileSetting_text():
    return profileSetting_text

def get_startText():
    return start_text

def get_getContactText():
    return getContact_text

def get_describeText():
    return start_reporting

def get_getAliasesText():
    return getAliases_text

def get_enterNewAliasText():
    return new_alias_while_reporting


def get_denyText():
    return deny_text


def getAliases_while_reporting_text():
    return get_alias_while_reporting_text



def get_illigalText():
    return illigal_text


def get_vegCleaningText():
    return vegCleaning_text


def get_regester_new_alias():
    return regester_new_alias_text

def send_report():
    return send_report_text


def selected_alias_goto_city():
    return selected_alias_goto_city_text


def city_selected_goto_report():
    return city_selected_goto_report_text


def get_add_new_alias():
    return get_add_new_alias_text
