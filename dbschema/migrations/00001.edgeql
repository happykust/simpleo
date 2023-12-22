CREATE MIGRATION m1mexkc56cdgblxr6br24rttzju3myyvguooyates4rv2zapmkk7vq
    ONTO initial
{
  CREATE MODULE auth IF NOT EXISTS;
  CREATE MODULE news IF NOT EXISTS;
  CREATE GLOBAL auth::current_user_id -> std::uuid;
  CREATE ABSTRACT TYPE default::Auditable {
      CREATE PROPERTY created_at: std::datetime {
          SET default := (std::datetime_current());
          SET readonly := true;
      };
      CREATE PROPERTY updated_at: std::datetime {
          CREATE REWRITE
              UPDATE 
              USING (std::datetime_of_statement());
      };
  };
  CREATE TYPE auth::User EXTENDING default::Auditable {
      CREATE REQUIRED PROPERTY email: std::str;
      CREATE REQUIRED PROPERTY password: std::str;
      CREATE REQUIRED PROPERTY username: std::str {
          CREATE CONSTRAINT std::exclusive;
      };
      CREATE ACCESS POLICY self_user_has_full_access
          ALLOW ALL USING ((GLOBAL auth::current_user_id ?= .id)) {
              SET errmessage := 'You cannot manage other users';
          };
      CREATE ACCESS POLICY user_can_be_registered
          ALLOW SELECT, INSERT USING ((GLOBAL auth::current_user_id ?= <std::uuid>{}));
      CREATE INDEX ON ((.username, .email));
  };
  CREATE GLOBAL auth::current_user := (SELECT
      auth::User
  FILTER
      (.id = GLOBAL auth::current_user_id)
  );
  CREATE TYPE news::News EXTENDING default::Auditable {
      CREATE REQUIRED LINK user: auth::User;
      CREATE REQUIRED PROPERTY content: std::str;
      CREATE REQUIRED PROPERTY title: std::str;
  };
};
