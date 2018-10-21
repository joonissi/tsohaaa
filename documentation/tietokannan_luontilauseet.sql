CREATE TABLE account (
        id INTEGER NOT NULL, 
        username VARCHAR(144) NOT NULL, 
        password VARCHAR(144) NOT NULL, 
        email VARCHAR(144) NOT NULL, 
        created_at DATETIME, 
        updated_at DATETIME, 
        PRIMARY KEY (id), 
        UNIQUE (username)
);
CREATE TABLE message (
        id INTEGER NOT NULL, 
        message TEXT, 
        created_at DATETIME, 
        updated_at DATETIME, 
        PRIMARY KEY (id)
);
CREATE TABLE conversations (
        account_id INTEGER NOT NULL, 
        message_id INTEGER NOT NULL, 
        PRIMARY KEY (account_id, message_id), 
        FOREIGN KEY(account_id) REFERENCES account (id), 
        FOREIGN KEY(message_id) REFERENCES message (id)
);
CREATE TABLE photo (
        id INTEGER NOT NULL, 
        link VARCHAR(150) NOT NULL, 
        details VARCHAR(250), 
        active BOOLEAN NOT NULL, 
        created_at DATETIME, 
        updated_at DATETIME, 
        account_id INTEGER NOT NULL, 
        PRIMARY KEY (id), 
        CHECK (active IN (0, 1)), 
        FOREIGN KEY(account_id) REFERENCES account (id)
);
