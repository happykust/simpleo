module news {
    type News extending default::Auditable {
        required user: auth::User;
        required title: str;
        required content: str;
    }
}