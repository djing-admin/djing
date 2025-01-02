class WithBadge:
    def with_badge(self, badge, badge_type="info"):
        self._badge = badge
        self._badge_type = badge_type

        return self
