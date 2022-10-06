from typing import Dict, Optional, Tuple
from django.shortcuts import render, redirect
from django.views import View
from core.models import UserDetail, Symbols
from core.utils import (
    generate_roll_values,
    re_roll_probability_30,
    re_roll_probability_60
)


class StartGame(View):
    template_name: str = "start_game.html"

    def get(self, request):
        return render(request, self.template_name)


class CreateUserSession(View):
    template_name: str = "user_detail.html"

    def get(self, request):
        user_uuid: Optional[str] = request.session.get("user_uuid")
        if user_uuid:
            return redirect("casino")
        return render(request, self.template_name)

    def post(self, request):
        email: Optional[str] = request.POST.get("email")
        first_name: Optional[str] = request.POST.get("first_name")
        last_name: Optional[str] = request.POST.get("last_name")

        user, is_created = UserDetail.objects.get_or_create(
            email=email, first_name=first_name, last_name=last_name
        )
        if user.is_active is False:
            user.is_active = True
            user.credit = 10
            user.save()
        request.session['user_uuid'] = user.uuid.__str__()
        return redirect('casino')


class casinoView(View):
    template_name: str = "casino.html"

    def get(self, request):
        user_uuid: Optional[str] = request.session.get("user_uuid")
        if not user_uuid:
            redirect("/")
        user: UserDetail = UserDetail.objects.get(uuid=user_uuid)
        context: Dict = {
            "uuid": user.uuid.__str__(),
            "full_name": f"{user.first_name} {user.last_name}",
            "credit": user.credit,
            "symbols": [0, 0, 0]
        }
        return render(request, self.template_name, locals())


class RollView(View):
    template_name: str = "casino.html"

    def generate_symbols(self, values: Tuple) -> Tuple:
        return tuple(Symbols.objects.get(id=symbol).represent for symbol in values)

    def check_win(self, choices: Tuple) -> Tuple:
        values: Tuple = generate_roll_values(3, choices)
        symbols: Tuple = self.generate_symbols(values)
        block_1, block_2, block_3 = values
        return block_1 == block_2 and block_1 == block_3, block_1, symbols

    def get(self, request):
        user_uuid: Optional[str] = request.session.get("user_uuid")
        if not user_uuid:
            redirect("/")
        user = UserDetail.objects.get(uuid=user_uuid)
        existing_credits: int = user.credit
        if existing_credits == 0:
            return redirect('close_session')
        roll_values: Tuple = tuple(Symbols.objects.values_list("id", flat=True))
        win, block, symbols = self.check_win(roll_values)
        is_re_roll = 0
        run = False
        if win:
            if existing_credits >= 40 and existing_credits < 60:
                is_re_roll: int = re_roll_probability_30()
                run = True
            elif existing_credits >= 60:
                is_re_roll: int = re_roll_probability_60()
                run = True
            else:
                user.credit += Symbols.objects.get(id=block).reward
            if run:
                if is_re_roll:
                    win, block, symbols = self.check_win(roll_values)
                    if win:
                        user.credit += Symbols.objects.get(id=block).reward
                else:
                    values: Tuple = generate_roll_values(3, roll_values)
                    symbols = self.generate_symbols(values)

        user.credit -= 1
        user.save()
        context: Dict = {
            "uuid": user.uuid.__str__(),
            "full_name": f"{user.first_name} {user.last_name}",
            "credit": user.credit,
            "symbols": symbols
        }
        return render(request, self.template_name, locals())


class CloseSessionView(View):
    def get(self, request):
        user_uuid: Optional[str] = request.session.get("user_uuid")
        if not user_uuid:
            redirect("/")
        user: UserDetail = UserDetail.objects.get(uuid=user_uuid)
        user.is_active = False
        user.credit = 0
        user.save()
        del request.session["user_uuid"]
        return redirect("/")
