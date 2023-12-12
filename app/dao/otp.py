from datetime import datetime, timedelta
from sqlalchemy import and_
from app.models.otp import Otp
from db import db


class OtpDAO:
    @staticmethod
    def get_otp_by_email(email: str) -> Otp:
        current_time = datetime.utcnow()
        print(current_time)
        time_diff = current_time - timedelta(minutes=10)
        otp: Otp = (Otp.query.filter(and_(Otp.email == email,
                                          Otp.created_at >= time_diff,
                                          Otp.created_at <= current_time)
                                     ).order_by(Otp.id.desc()).first())
        return otp if otp else {}

    @staticmethod
    def delete_otp(email: str) -> None:
        email: Otp = Otp.query.filter_by(email=email)
        if email:
            email.delete()
        db.session.commit()

