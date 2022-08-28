

CREATE TABLE IF NOT EXISTS `TeleInformation` 
(
    `id` INT NOT NULL AUTO_INCREMENT,
    `created_at` datetime default CURRENT_TIMESTAMP,
    `MSISDN` VARCHAR(200) DEFAULT NULL,
    `handset_type` VARCHAR(200) DEFAULT NULL,
    `average_tcp` FLOAT DEFAULT NULL,
    `average_rtt` FLOAT DEFAULT NULL,
    `average_throughput` FLOAT DEFAULT NULL,
    `session_frequency` FLOAT DEFAULT NULL,
    `session_duration` FLOAT DEFAULT NULL,
    `total_dl_and_ul_data` FLOAT DEFAULT NULL,
    `engagement_score` FLOAT DEFAULT NULL,
    `experience_score` FLOAT DEFAULT NULL,
    `satisfaction_score` FLOAT DEFAULT NULL,
    `handset_manufacturer` VARCHAR(200) DEFAULT NULL,
    `social_total` FLOAT DEFAULT NULL,
    `google_total` FLOAT DEFAULT NULL,
    `email_total` FLOAT DEFAULT NULL,
    `youtube_total` FLOAT DEFAULT NULL,
    `netflix_total` FLOAT DEFAULT NULL,
    `gaming_total` FLOAT DEFAULT NULL,
    `other_total` FLOAT DEFAULT NULL,
    PRIMARY KEY (`id`)
)
ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE utf8mb4_unicode_ci;




