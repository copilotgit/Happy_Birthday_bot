from .start import dp as start_dp
from .help import dp as help_dp
from .registration import dp as reg_dp
from .user import dp as user_dp
from .echo import dp as echo_dp

routers = [help_dp, reg_dp, start_dp, user_dp, echo_dp]