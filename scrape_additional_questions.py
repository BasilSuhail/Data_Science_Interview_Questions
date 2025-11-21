#!/usr/bin/env python3
"""
Aggressive Question Scraper for Data Science Interview Questions
Scrapes from: LeetCode Discuss, Glassdoor (public), Reddit, GitHub

Author: AI Interview Coach
Date: 2025-11-21
"""

import requests
from bs4 import BeautifulSoup
import csv
import time
import json
from datetime import datetime
import random

class QuestionScraper:
    def __init__(self, output_file="scraped_questions.csv"):
        self.output_file = output_file
        self.questions = []
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }

    def scrape_reddit_datascience(self):
        """Scrape data science interview questions from Reddit"""
        print("🔍 Scraping Reddit r/datascience...")

        subreddits = [
            'datascience',
            'MachineLearning',
            'learnmachinelearning',
            'cscareerquestions'
        ]

        search_terms = [
            'interview questions',
            'data science interview',
            'ML interview',
            'statistics interview'
        ]

        for subreddit in subreddits:
            for term in search_terms:
                try:
                    # Use Reddit's JSON API (no auth needed for public posts)
                    url = f"https://www.reddit.com/r/{subreddit}/search.json?q={term.replace(' ', '+')}&restrict_sr=1&limit=25"
                    response = requests.get(url, headers=self.headers)

                    if response.status_code == 200:
                        data = response.json()
                        posts = data.get('data', {}).get('children', [])

                        for post in posts:
                            post_data = post.get('data', {})
                            title = post_data.get('title', '')
                            selftext = post_data.get('selftext', '')

                            # Extract questions from post
                            questions = self._extract_questions_from_text(title + "\n" + selftext)

                            for q in questions:
                                self.questions.append({
                                    'question_text': q,
                                    'company': '',
                                    'difficulty': 'medium',
                                    'question_type': self._infer_question_type(q),
                                    'topics': self._extract_topics(q),
                                    'source': f'reddit-{subreddit}',
                                    'answer_text': '',
                                    'created_at': datetime.now().isoformat()
                                })

                        print(f"  ✅ Found {len(posts)} posts from r/{subreddit}")
                        time.sleep(2)  # Rate limiting

                except Exception as e:
                    print(f"  ⚠️  Error scraping r/{subreddit}: {e}")
                    continue

    def scrape_github_repos(self):
        """Scrape interview question repos from GitHub"""
        print("🔍 Scraping GitHub interview question repos...")

        repos = [
            'https://raw.githubusercontent.com/alexeygrigorev/data-science-interviews/master/theory.md',
            'https://raw.githubusercontent.com/khanhnamle1994/cracking-the-data-science-interview/master/Question-Bank/Data-Science-Prep.md',
            'https://raw.githubusercontent.com/iamtodor/data-science-interview-questions-and-answers/master/README.md'
        ]

        for repo_url in repos:
            try:
                response = requests.get(repo_url, headers=self.headers)

                if response.status_code == 200:
                    text = response.text
                    questions = self._extract_questions_from_markdown(text)

                    for q in questions:
                        self.questions.append({
                            'question_text': q,
                            'company': '',
                            'difficulty': 'medium',
                            'question_type': self._infer_question_type(q),
                            'topics': self._extract_topics(q),
                            'source': 'github',
                            'answer_text': '',
                            'created_at': datetime.now().isoformat()
                        })

                    print(f"  ✅ Scraped {len(questions)} questions from {repo_url.split('/')[-2]}")
                    time.sleep(1)

            except Exception as e:
                print(f"  ⚠️  Error scraping {repo_url}: {e}")
                continue

    def scrape_leetcode_discuss(self):
        """Scrape LeetCode Discuss data science topics"""
        print("🔍 Scraping LeetCode Discuss...")

        # LeetCode discuss topics (public, no auth)
        topics = [
            'data-science',
            'interview-question',
            'statistics'
        ]

        for topic in topics:
            try:
                url = f"https://leetcode.com/discuss/interview-question?tags={topic}"
                response = requests.get(url, headers=self.headers)

                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')

                    # Extract question titles from discuss posts
                    titles = soup.find_all('a', class_='topic-title')

                    for title in titles[:20]:  # Limit to 20 per topic
                        question = title.get_text(strip=True)

                        if len(question) > 20:  # Valid question
                            self.questions.append({
                                'question_text': question,
                                'company': self._extract_company_from_text(question),
                                'difficulty': 'medium',
                                'question_type': self._infer_question_type(question),
                                'topics': self._extract_topics(question),
                                'source': 'leetcode',
                                'answer_text': '',
                                'created_at': datetime.now().isoformat()
                            })

                    print(f"  ✅ Scraped {len(titles[:20])} questions from LeetCode/{topic}")
                    time.sleep(3)  # Rate limiting

            except Exception as e:
                print(f"  ⚠️  Error scraping LeetCode: {e}")
                continue

    def scrape_glassdoor_public(self):
        """Scrape public Glassdoor interview questions (no login required)"""
        print("🔍 Scraping Glassdoor public interview questions...")

        companies = [
            'Meta', 'Google', 'Amazon', 'Microsoft', 'Netflix',
            'Apple', 'Tesla', 'Uber', 'Airbnb', 'LinkedIn'
        ]

        for company in companies:
            try:
                # Glassdoor public search (no auth)
                url = f"https://www.glassdoor.com/Interview/{company.replace(' ', '-')}-Interview-Questions-E{random.randint(1000, 99999)}.htm"

                # Note: Glassdoor blocks scrapers heavily, so this might not work
                # We'll try but expect it to fail
                response = requests.get(url, headers=self.headers, timeout=10)

                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')

                    # Try to extract questions (this selector may change)
                    questions_elements = soup.find_all('span', class_='question')

                    for q_elem in questions_elements[:10]:
                        question = q_elem.get_text(strip=True)

                        if len(question) > 20:
                            self.questions.append({
                                'question_text': question,
                                'company': company,
                                'difficulty': 'medium',
                                'question_type': self._infer_question_type(question),
                                'topics': self._extract_topics(question),
                                'source': 'glassdoor',
                                'answer_text': '',
                                'created_at': datetime.now().isoformat()
                            })

                    print(f"  ✅ Scraped questions from Glassdoor/{company}")
                    time.sleep(5)  # Longer delay for Glassdoor

            except Exception as e:
                print(f"  ⚠️  Glassdoor blocked or error for {company}: {e}")
                continue

    def _extract_questions_from_text(self, text):
        """Extract questions from raw text"""
        questions = []

        # Look for sentences ending with ?
        lines = text.split('\n')
        for line in lines:
            line = line.strip()
            if '?' in line and len(line) > 20:
                questions.append(line)

        return questions

    def _extract_questions_from_markdown(self, text):
        """Extract questions from markdown format"""
        questions = []

        lines = text.split('\n')
        for line in lines:
            line = line.strip()

            # Look for markdown list items with questions
            if (line.startswith('- ') or line.startswith('* ') or
                line.startswith('+ ') or line.startswith('1.')):
                question = line.lstrip('-*+0123456789. ').strip()
                if len(question) > 20:
                    questions.append(question)

            # Look for lines ending with ?
            elif '?' in line and len(line) > 20:
                questions.append(line)

        return questions

    def _infer_question_type(self, question):
        """Infer question type from question text"""
        q_lower = question.lower()

        if any(word in q_lower for word in ['code', 'algorithm', 'implement', 'write', 'python', 'sql', 'query']):
            return 'coding'
        elif any(word in q_lower for word in ['probability', 'statistics', 'hypothesis', 'distribution', 'variance']):
            return 'stats'
        elif any(word in q_lower for word in ['model', 'machine learning', 'neural', 'regression', 'classification', 'deep learning']):
            return 'ml'
        elif any(word in q_lower for word in ['case study', 'estimate', 'product', 'business', 'metric']):
            return 'case'
        elif any(word in q_lower for word in ['tell me about', 'describe', 'explain your', 'weakness', 'strength']):
            return 'behavioral'
        else:
            return 'mixed'

    def _extract_topics(self, question):
        """Extract topics from question text"""
        topics = []
        q_lower = question.lower()

        topic_keywords = {
            'regression': ['regression', 'linear regression', 'logistic regression'],
            'classification': ['classification', 'classifier'],
            'clustering': ['clustering', 'k-means', 'hierarchical'],
            'neural_network': ['neural', 'deep learning', 'cnn', 'rnn', 'lstm'],
            'probability': ['probability', 'bayes', 'conditional'],
            'statistics': ['statistics', 'hypothesis', 'test', 'anova', 'variance'],
            'python': ['python', 'pandas', 'numpy'],
            'sql': ['sql', 'database', 'query'],
            'nlp': ['nlp', 'text', 'language model'],
            'computer_vision': ['computer vision', 'image', 'cnn'],
            'feature_engineering': ['feature', 'engineering', 'selection'],
            'ensemble': ['ensemble', 'random forest', 'boosting', 'bagging']
        }

        for topic, keywords in topic_keywords.items():
            if any(kw in q_lower for kw in keywords):
                topics.append(topic)

        return '|'.join(topics) if topics else ''

    def _extract_company_from_text(self, text):
        """Extract company name from question text"""
        companies = [
            'Meta', 'Google', 'Amazon', 'Microsoft', 'Netflix',
            'Apple', 'Tesla', 'Uber', 'Airbnb', 'LinkedIn',
            'Facebook', 'Twitter', 'Spotify', 'Stripe', 'Snap'
        ]

        for company in companies:
            if company.lower() in text.lower():
                return company

        return ''

    def save_to_csv(self):
        """Save scraped questions to CSV"""
        if not self.questions:
            print("⚠️  No questions scraped!")
            return

        print(f"\n💾 Saving {len(self.questions)} questions to {self.output_file}...")

        with open(self.output_file, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['question_text', 'company', 'difficulty', 'question_type',
                         'topics', 'source', 'answer_text', 'created_at']
            writer = csv.DictWriter(f, fieldnames=fieldnames)

            writer.writeheader()
            writer.writerows(self.questions)

        print(f"✅ Saved successfully!")

        # Print stats
        print(f"\n📊 Scraping Stats:")
        print(f"  Total questions: {len(self.questions)}")

        by_source = {}
        for q in self.questions:
            source = q['source']
            by_source[source] = by_source.get(source, 0) + 1

        for source, count in sorted(by_source.items(), key=lambda x: -x[1]):
            print(f"  {source}: {count}")

    def run_all(self):
        """Run all scrapers"""
        print("🚀 Starting aggressive question scraping...\n")

        # Run scrapers
        self.scrape_github_repos()
        print()

        self.scrape_reddit_datascience()
        print()

        self.scrape_leetcode_discuss()
        print()

        self.scrape_glassdoor_public()
        print()

        # Save results
        self.save_to_csv()

        print("\n✅ Scraping complete!")

if __name__ == "__main__":
    scraper = QuestionScraper(output_file="scraped_questions.csv")
    scraper.run_all()
