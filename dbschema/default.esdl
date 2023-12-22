module default {
    abstract type Auditable {
        created_at: datetime {
            default := (datetime_current());
            readonly := true;
        };
        updated_at: datetime {
          rewrite update using (datetime_of_statement());
        };
    };
}
