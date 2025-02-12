
class UserVerifyMixin:
    checked_user = None
    
    def check_user_exists(self, username: str) -> bool:
        self.checked_user = self.db_session.query(self.user_model).where(self.user_model.username==username).all()
        if len(self.checked_user) > 0:
            return True
        return False
    
    def check_user_by_id(self, user_id: int) -> bool:
        self.checked_user = self.db_session.query(self.user_model).where(self.user_model.id==user_id).one_or_none()
        if self.checked_user and self.checked_user.active:
            return True
        return False