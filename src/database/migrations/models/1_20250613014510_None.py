from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "habit_templates" (
    "id" CHAR(36) NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "deleted_at" TIMESTAMP,
    "name" VARCHAR(255) NOT NULL,
    "description" TEXT,
    "category" VARCHAR(100) NOT NULL,
    "default_frequency" VARCHAR(7) NOT NULL /* DAILY: daily\nWEEKLY: weekly\nMONTHLY: monthly\nYEARLY: yearly */,
    "default_target_days" JSON,
    "default_target_count" INT NOT NULL DEFAULT 1,
    "default_reminder_time" TIME NOT NULL DEFAULT '09:00:00',
    "icon_name" VARCHAR(50),
    "color" VARCHAR(7) NOT NULL DEFAULT '#4CAF50',
    "difficulty_level" INT NOT NULL DEFAULT 1,
    "estimated_time_minutes" INT,
    "is_active" INT NOT NULL DEFAULT 1,
    "sort_order" INT NOT NULL DEFAULT 0
);
CREATE INDEX IF NOT EXISTS "idx_habit_templ_name_e6395e" ON "habit_templates" ("name");
CREATE INDEX IF NOT EXISTS "idx_habit_templ_categor_5030e7" ON "habit_templates" ("category");
CREATE INDEX IF NOT EXISTS "idx_habit_templ_is_acti_deab81" ON "habit_templates" ("is_active");
CREATE INDEX IF NOT EXISTS "idx_habit_templ_categor_d5692c" ON "habit_templates" ("category", "is_active");
CREATE INDEX IF NOT EXISTS "idx_habit_templ_sort_or_2e0656" ON "habit_templates" ("sort_order");
CREATE TABLE IF NOT EXISTS "habit_template_messages" (
    "id" CHAR(36) NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "deleted_at" TIMESTAMP,
    "message_type" VARCHAR(13) NOT NULL /* REMINDER: reminder\nENCOURAGEMENT: encouragement\nSTREAK: streak\nMISSED: missed */,
    "message_text" TEXT NOT NULL,
    "is_active" INT NOT NULL DEFAULT 1,
    "usage_count" INT NOT NULL DEFAULT 0,
    "habit_template_id" CHAR(36) NOT NULL REFERENCES "habit_templates" ("id") ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS "idx_habit_templ_message_0f1e1a" ON "habit_template_messages" ("message_type");
CREATE INDEX IF NOT EXISTS "idx_habit_templ_habit_t_ab358f" ON "habit_template_messages" ("habit_template_id");
CREATE INDEX IF NOT EXISTS "idx_habit_templ_habit_t_233895" ON "habit_template_messages" ("habit_template_id", "message_type", "is_active");
CREATE TABLE IF NOT EXISTS "recurrence_patterns" (
    "id" CHAR(36) NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "deleted_at" TIMESTAMP,
    "frequency" VARCHAR(7) NOT NULL /* DAILY: daily\nWEEKLY: weekly\nMONTHLY: monthly\nYEARLY: yearly */,
    "interval_value" INT NOT NULL DEFAULT 1,
    "days_of_week" JSON,
    "day_of_month" INT,
    "month_of_year" INT,
    "end_type" VARCHAR(20) NOT NULL DEFAULT 'never',
    "end_count" INT,
    "end_date" DATE
);
CREATE TABLE IF NOT EXISTS "users" (
    "id" CHAR(36) NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "deleted_at" TIMESTAMP,
    "clerk_id" VARCHAR(255) NOT NULL UNIQUE,
    "email" VARCHAR(255) NOT NULL UNIQUE,
    "username" VARCHAR(100),
    "timezone" VARCHAR(50) NOT NULL DEFAULT 'UTC',
    "default_reminder_minutes" INT NOT NULL DEFAULT 15,
    "preferred_notification_type" VARCHAR(8) NOT NULL DEFAULT 'push' /* EMAIL: email\nPUSH: push\nWEB_PUSH: web_push */
);
CREATE INDEX IF NOT EXISTS "idx_users_clerk_i_f06c0c" ON "users" ("clerk_id");
CREATE INDEX IF NOT EXISTS "idx_users_email_133a6f" ON "users" ("email");
CREATE INDEX IF NOT EXISTS "idx_users_email_3ff49e" ON "users" ("email", "clerk_id");
CREATE TABLE IF NOT EXISTS "calendars" (
    "id" CHAR(36) NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "deleted_at" TIMESTAMP,
    "name" VARCHAR(255) NOT NULL,
    "description" TEXT,
    "color" VARCHAR(7) NOT NULL DEFAULT '#3174ad',
    "is_default" INT NOT NULL DEFAULT 0,
    "user_id" CHAR(36) NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS "idx_calendars_user_id_5fb33b" ON "calendars" ("user_id");
CREATE TABLE IF NOT EXISTS "categories" (
    "id" CHAR(36) NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "deleted_at" TIMESTAMP,
    "name" VARCHAR(100) NOT NULL,
    "color" VARCHAR(7) NOT NULL DEFAULT '#666666',
    "user_id" CHAR(36) NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS "idx_categories_user_id_b282c5" ON "categories" ("user_id");
CREATE TABLE IF NOT EXISTS "events" (
    "id" CHAR(36) NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "deleted_at" TIMESTAMP,
    "title" VARCHAR(500) NOT NULL,
    "description" TEXT,
    "location" VARCHAR(500),
    "start_datetime" TIMESTAMP NOT NULL,
    "end_datetime" TIMESTAMP NOT NULL,
    "is_all_day" INT NOT NULL DEFAULT 0,
    "is_recurring_master" INT NOT NULL DEFAULT 0,
    "status" VARCHAR(9) NOT NULL DEFAULT 'confirmed' /* CONFIRMED: confirmed\nTENTATIVE: tentative\nCANCELLED: cancelled */,
    "priority" SMALLINT NOT NULL DEFAULT 0 /* NONE: 0\nLOW: 1\nMEDIUM: 2\nHIGH: 3\nURGENT: 4 */,
    "calendar_id" CHAR(36) NOT NULL REFERENCES "calendars" ("id") ON DELETE CASCADE,
    "parent_event_id" CHAR(36) REFERENCES "events" ("id") ON DELETE CASCADE,
    "recurrence_pattern_id" CHAR(36) REFERENCES "recurrence_patterns" ("id") ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS "idx_events_title_44f4d6" ON "events" ("title");
CREATE INDEX IF NOT EXISTS "idx_events_start_d_6bb698" ON "events" ("start_datetime");
CREATE INDEX IF NOT EXISTS "idx_events_end_dat_019d54" ON "events" ("end_datetime");
CREATE INDEX IF NOT EXISTS "idx_events_is_recu_ba15e6" ON "events" ("is_recurring_master");
CREATE INDEX IF NOT EXISTS "idx_events_status_c1e5d2" ON "events" ("status");
CREATE INDEX IF NOT EXISTS "idx_events_calenda_262f7f" ON "events" ("calendar_id");
CREATE INDEX IF NOT EXISTS "idx_events_start_d_56bb23" ON "events" ("start_datetime", "end_datetime");
CREATE INDEX IF NOT EXISTS "idx_events_status_077525" ON "events" ("status", "start_datetime");
CREATE TABLE IF NOT EXISTS "event_category_mappings" (
    "id" CHAR(36) NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "deleted_at" TIMESTAMP,
    "category_id" CHAR(36) NOT NULL REFERENCES "categories" ("id") ON DELETE CASCADE,
    "event_id" CHAR(36) NOT NULL REFERENCES "events" ("id") ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS "idx_event_categ_event_i_f2de3c" ON "event_category_mappings" ("event_id");
CREATE INDEX IF NOT EXISTS "idx_event_categ_categor_aa7aab" ON "event_category_mappings" ("category_id");
CREATE TABLE IF NOT EXISTS "event_exceptions" (
    "id" CHAR(36) NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "deleted_at" TIMESTAMP,
    "exception_date" DATE NOT NULL,
    "exception_type" VARCHAR(20) NOT NULL,
    "master_event_id" CHAR(36) NOT NULL REFERENCES "events" ("id") ON DELETE CASCADE,
    "modified_event_id" CHAR(36) REFERENCES "events" ("id") ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS "idx_event_excep_master__501464" ON "event_exceptions" ("master_event_id", "exception_date");
CREATE TABLE IF NOT EXISTS "event_instances" (
    "id" CHAR(36) NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "deleted_at" TIMESTAMP,
    "instance_date" DATE NOT NULL,
    "start_datetime" TIMESTAMP NOT NULL,
    "end_datetime" TIMESTAMP NOT NULL,
    "is_exception" INT NOT NULL DEFAULT 0,
    "master_event_id" CHAR(36) NOT NULL REFERENCES "events" ("id") ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS "idx_event_insta_instanc_4858d5" ON "event_instances" ("instance_date");
CREATE INDEX IF NOT EXISTS "idx_event_insta_start_d_e3e2c4" ON "event_instances" ("start_datetime");
CREATE INDEX IF NOT EXISTS "idx_event_insta_end_dat_3c051f" ON "event_instances" ("end_datetime");
CREATE INDEX IF NOT EXISTS "idx_event_insta_master__da14c3" ON "event_instances" ("master_event_id");
CREATE INDEX IF NOT EXISTS "idx_event_insta_master__1b845e" ON "event_instances" ("master_event_id", "instance_date");
CREATE INDEX IF NOT EXISTS "idx_event_insta_start_d_243b18" ON "event_instances" ("start_datetime", "end_datetime");
CREATE TABLE IF NOT EXISTS "event_reminders" (
    "id" CHAR(36) NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "deleted_at" TIMESTAMP,
    "reminder_minutes" INT NOT NULL,
    "notification_type" VARCHAR(8) NOT NULL /* EMAIL: email\nPUSH: push\nWEB_PUSH: web_push */,
    "is_enabled" INT NOT NULL DEFAULT 1,
    "event_id" CHAR(36) NOT NULL REFERENCES "events" ("id") ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS "idx_event_remin_event_i_227c51" ON "event_reminders" ("event_id");
CREATE TABLE IF NOT EXISTS "habits" (
    "id" CHAR(36) NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "deleted_at" TIMESTAMP,
    "name" VARCHAR(255) NOT NULL,
    "description" TEXT,
    "frequency" VARCHAR(7) NOT NULL /* DAILY: daily\nWEEKLY: weekly\nMONTHLY: monthly\nYEARLY: yearly */,
    "target_days" JSON,
    "target_count" INT NOT NULL DEFAULT 1,
    "reminder_time" TIME,
    "is_active" INT NOT NULL DEFAULT 1,
    "template_id" CHAR(36) REFERENCES "habit_templates" ("id") ON DELETE CASCADE,
    "user_id" CHAR(36) NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS "idx_habits_is_acti_d073af" ON "habits" ("is_active");
CREATE INDEX IF NOT EXISTS "idx_habits_user_id_ecc672" ON "habits" ("user_id");
CREATE INDEX IF NOT EXISTS "idx_habits_user_id_387b1a" ON "habits" ("user_id", "is_active");
CREATE INDEX IF NOT EXISTS "idx_habits_templat_234486" ON "habits" ("template_id");
CREATE TABLE IF NOT EXISTS "habit_completions" (
    "id" CHAR(36) NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "deleted_at" TIMESTAMP,
    "completion_date" DATE NOT NULL,
    "completed_count" INT NOT NULL DEFAULT 1,
    "notes" TEXT,
    "habit_id" CHAR(36) NOT NULL REFERENCES "habits" ("id") ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS "idx_habit_compl_complet_0c8c2d" ON "habit_completions" ("completion_date");
CREATE INDEX IF NOT EXISTS "idx_habit_compl_habit_i_fb965a" ON "habit_completions" ("habit_id");
CREATE INDEX IF NOT EXISTS "idx_habit_compl_habit_i_d0e90f" ON "habit_completions" ("habit_id", "completion_date");
CREATE TABLE IF NOT EXISTS "habit_streaks" (
    "id" CHAR(36) NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "deleted_at" TIMESTAMP,
    "start_date" DATE NOT NULL,
    "end_date" DATE,
    "streak_length" INT NOT NULL,
    "is_current" INT NOT NULL DEFAULT 0,
    "habit_id" CHAR(36) NOT NULL REFERENCES "habits" ("id") ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS "idx_habit_strea_is_curr_dc715a" ON "habit_streaks" ("is_current");
CREATE INDEX IF NOT EXISTS "idx_habit_strea_habit_i_d5533f" ON "habit_streaks" ("habit_id");
CREATE INDEX IF NOT EXISTS "idx_habit_strea_habit_i_3911a4" ON "habit_streaks" ("habit_id", "is_current");
CREATE INDEX IF NOT EXISTS "idx_habit_strea_habit_i_1f9583" ON "habit_streaks" ("habit_id", "start_date");
CREATE TABLE IF NOT EXISTS "tasks" (
    "id" CHAR(36) NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "deleted_at" TIMESTAMP,
    "title" VARCHAR(500) NOT NULL,
    "description" TEXT,
    "due_date" DATE,
    "due_time" TIME,
    "status" VARCHAR(11) NOT NULL DEFAULT 'pending' /* PENDING: pending\nIN_PROGRESS: in_progress\nCOMPLETED: completed\nCANCELLED: cancelled */,
    "priority" SMALLINT NOT NULL DEFAULT 1 /* NONE: 0\nLOW: 1\nMEDIUM: 2\nHIGH: 3\nURGENT: 4 */,
    "completion_percentage" INT NOT NULL DEFAULT 0,
    "estimated_duration" INT,
    "actual_duration" INT,
    "completed_at" TIMESTAMP,
    "category_id" CHAR(36) REFERENCES "categories" ("id") ON DELETE CASCADE,
    "parent_task_id" CHAR(36) REFERENCES "tasks" ("id") ON DELETE CASCADE,
    "recurrence_pattern_id" CHAR(36) REFERENCES "recurrence_patterns" ("id") ON DELETE CASCADE,
    "user_id" CHAR(36) NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS "idx_tasks_title_077193" ON "tasks" ("title");
CREATE INDEX IF NOT EXISTS "idx_tasks_due_dat_89d016" ON "tasks" ("due_date");
CREATE INDEX IF NOT EXISTS "idx_tasks_status_449504" ON "tasks" ("status");
CREATE INDEX IF NOT EXISTS "idx_tasks_priorit_236091" ON "tasks" ("priority");
CREATE INDEX IF NOT EXISTS "idx_tasks_user_id_7d4869" ON "tasks" ("user_id");
CREATE INDEX IF NOT EXISTS "idx_tasks_user_id_062b44" ON "tasks" ("user_id", "status");
CREATE INDEX IF NOT EXISTS "idx_tasks_due_dat_6d1447" ON "tasks" ("due_date", "priority");
CREATE INDEX IF NOT EXISTS "idx_tasks_status_acfeee" ON "tasks" ("status", "due_date");
CREATE INDEX IF NOT EXISTS "idx_tasks_parent__53afe3" ON "tasks" ("parent_task_id");
CREATE TABLE IF NOT EXISTS "task_dependencies" (
    "id" CHAR(36) NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "deleted_at" TIMESTAMP,
    "dependent_task_id" CHAR(36) NOT NULL REFERENCES "tasks" ("id") ON DELETE CASCADE,
    "prerequisite_task_id" CHAR(36) NOT NULL REFERENCES "tasks" ("id") ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS "idx_task_depend_depende_a00f2c" ON "task_dependencies" ("dependent_task_id");
CREATE INDEX IF NOT EXISTS "idx_task_depend_prerequ_6e0f4b" ON "task_dependencies" ("prerequisite_task_id");
CREATE TABLE IF NOT EXISTS "task_reminders" (
    "id" CHAR(36) NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "deleted_at" TIMESTAMP,
    "reminder_minutes" INT NOT NULL,
    "notification_type" VARCHAR(8) NOT NULL /* EMAIL: email\nPUSH: push\nWEB_PUSH: web_push */,
    "is_enabled" INT NOT NULL DEFAULT 1,
    "task_id" CHAR(36) NOT NULL REFERENCES "tasks" ("id") ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS "idx_task_remind_task_id_9107e9" ON "task_reminders" ("task_id");
CREATE TABLE IF NOT EXISTS "notification_queue" (
    "id" CHAR(36) NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "deleted_at" TIMESTAMP,
    "scheduled_time" TIMESTAMP NOT NULL,
    "notification_type" VARCHAR(8) NOT NULL /* EMAIL: email\nPUSH: push\nWEB_PUSH: web_push */,
    "status" VARCHAR(7) NOT NULL DEFAULT 'pending' /* PENDING: pending\nSENT: sent\nFAILED: failed */,
    "custom_message" TEXT,
    "message_type" VARCHAR(13) /* REMINDER: reminder\nENCOURAGEMENT: encouragement\nSTREAK: streak\nMISSED: missed */,
    "retry_count" INT NOT NULL DEFAULT 0,
    "error_message" TEXT,
    "sent_at" TIMESTAMP,
    "event_id" CHAR(36) REFERENCES "events" ("id") ON DELETE CASCADE,
    "event_reminder_id" CHAR(36) REFERENCES "event_reminders" ("id") ON DELETE CASCADE,
    "habit_id" CHAR(36) REFERENCES "habits" ("id") ON DELETE CASCADE,
    "task_id" CHAR(36) REFERENCES "tasks" ("id") ON DELETE CASCADE,
    "task_reminder_id" CHAR(36) REFERENCES "task_reminders" ("id") ON DELETE CASCADE,
    "user_id" CHAR(36) NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS "idx_notificatio_schedul_11a671" ON "notification_queue" ("scheduled_time");
CREATE INDEX IF NOT EXISTS "idx_notificatio_status_2935b5" ON "notification_queue" ("status");
CREATE INDEX IF NOT EXISTS "idx_notificatio_event_i_0f5d68" ON "notification_queue" ("event_id");
CREATE INDEX IF NOT EXISTS "idx_notificatio_habit_i_9cd507" ON "notification_queue" ("habit_id");
CREATE INDEX IF NOT EXISTS "idx_notificatio_task_id_ae321e" ON "notification_queue" ("task_id");
CREATE INDEX IF NOT EXISTS "idx_notificatio_user_id_407571" ON "notification_queue" ("user_id");
CREATE INDEX IF NOT EXISTS "idx_notificatio_schedul_5aafa8" ON "notification_queue" ("scheduled_time", "status");
CREATE INDEX IF NOT EXISTS "idx_notificatio_user_id_0152f8" ON "notification_queue" ("user_id", "status");
CREATE INDEX IF NOT EXISTS "idx_notificatio_status_a7ed67" ON "notification_queue" ("status", "retry_count");
CREATE TABLE IF NOT EXISTS "task_time_logs" (
    "id" CHAR(36) NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "deleted_at" TIMESTAMP,
    "start_time" TIMESTAMP NOT NULL,
    "end_time" TIMESTAMP,
    "duration_minutes" INT,
    "notes" TEXT,
    "task_id" CHAR(36) NOT NULL REFERENCES "tasks" ("id") ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS "idx_task_time_l_task_id_b26153" ON "task_time_logs" ("task_id");
CREATE INDEX IF NOT EXISTS "idx_task_time_l_task_id_3c515b" ON "task_time_logs" ("task_id", "start_time");
CREATE TABLE IF NOT EXISTS "user_devices" (
    "id" CHAR(36) NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "deleted_at" TIMESTAMP,
    "device_type" VARCHAR(7) NOT NULL /* WEB: web\nIOS: ios\nANDROID: android\nDESKTOP: desktop */,
    "push_token" TEXT,
    "endpoint_url" TEXT,
    "is_active" INT NOT NULL DEFAULT 1,
    "user_id" CHAR(36) NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS "idx_user_device_user_id_80f8d8" ON "user_devices" ("user_id");
CREATE INDEX IF NOT EXISTS "idx_user_device_user_id_80b679" ON "user_devices" ("user_id", "is_active");
CREATE INDEX IF NOT EXISTS "idx_user_device_device__8d3ea1" ON "user_devices" ("device_type");
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSON NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
