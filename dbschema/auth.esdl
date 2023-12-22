module auth {

    global current_user_id: uuid;
    global current_user := (
        select auth::User filter .id = global current_user_id
    );

    type User extending default::Auditable {
        required username: str {
            constraint exclusive;
        };
        required email: str;
        required password: str;

        index on ((.username, .email));

        access policy self_user_has_full_access allow all using (global current_user_id ?= .id) {
            errmessage := "You cannot manage other users"
        };
        access policy user_can_be_registered allow insert, select using (global current_user_id ?= <uuid>{});
    }

}