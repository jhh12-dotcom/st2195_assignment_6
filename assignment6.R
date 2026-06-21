library(dplyr)
library(tidyr)
library(stringr)

# --- Step 1: Load and Merge Datasets ---
speeches <- read.csv("speeches.csv") %>% select(date, contents)
fx <- read.csv("fx.csv")

# Standardize column names
colnames(fx) <- tolower(colnames(fx))
if("obs_value" %in% colnames(fx))) {
  fx <- fx %>% rename(rate = obs_value)
}

speeches$date <- as.Date(speeches$date)
fx$date <- as.Date(fx$date)

# Merge keeping all rows from fx
df <- fx %>% left_join(speeches, by = "date")

# --- Step 2: Remove obvious outliers or mistakes ---
df$rate <- as.numeric(df$rate)
df <- df %>% filter(!is.na(rate) & rate > 0)

# --- Step 3: Handle missing observations ---
df <- df %>% 
  arrange(date) %>% 
  fill(rate, .direction = "down") %>% 
  filter(!is.na(rate))

# --- Step 4: Calculate Return and Indicators ---
df <- df %>% 
  mutate(
    return = (rate - lag(rate)) / lag(rate),
    good_news = ifelse(!is.na(return) & return > 0.005, 1, 0),
    bad_news = ifelse(!is.na(return) & return < -0.005, 1, 0)
  )

# --- Step 5: Text Processing & Top 20 Words ---
df_text <- df %>% filter(!is.na(contents))

stopwords <- c("the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "with", 
               "by", "of", "from", "is", "are", "was", "were", "be", "been", "this", "that", 
               "it", "as", "by", "not", "by", "we", "our", "will", "have", "has", "can")

get_top_words <- function(text_vector, n = 20) {
  words <- text_vector %>% 
    str_to_lower() %>% 
    str_extract_all("\\b[a-z]{3,}\\b") %>% 
    unlist()
  
  words <- words[!words %in% stopwords]
  
  as.data.frame(table(words)) %>% 
    arrange(desc(Freq)) %>% 
    head(n) %>% 
    rename(word = words, count = Freq)
}

good_indicators <- get_top_words(df_text$contents[df_text$good_news == 1])
bad_indicators <- get_top_words(df_text$contents[df_text$bad_news == 1])

# Save to CSV
write.csv(good_indicators, "good_indicators.csv", row.names = FALSE)
write.csv(bad_indicators, "bad_indicators.csv", row.names = FALSE)

print("R execution complete. CSV files generated.")
