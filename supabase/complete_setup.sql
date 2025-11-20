-- ========================================
-- COMPLETE DATABASE SETUP - ALL IN ONE
-- Run this single script to set up everything
-- ========================================

-- ========================================
-- PART 1: CREATE TABLES
-- ========================================

-- DOCUMENTS TABLE (for textbooks)
CREATE TABLE IF NOT EXISTS documents (
    id BIGSERIAL PRIMARY KEY,
    book_name TEXT NOT NULL,
    page_number INTEGER,
    content TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create index for faster text searches
CREATE INDEX IF NOT EXISTS idx_documents_content
ON documents USING gin(to_tsvector('english', content));

-- Create index for book filtering
CREATE INDEX IF NOT EXISTS idx_documents_book
ON documents(book_name);

-- Create index for page number
CREATE INDEX IF NOT EXISTS idx_documents_page
ON documents(page_number);

-- INTERVIEW_QUESTIONS TABLE
CREATE TABLE IF NOT EXISTS interview_questions (
    id BIGSERIAL PRIMARY KEY,
    question TEXT,
    question_text TEXT,
    company TEXT,
    difficulty TEXT,
    question_type TEXT,
    topics TEXT,
    source TEXT,
    answer_text TEXT,
    category TEXT,
    tags TEXT,
    constraints TEXT,
    examples TEXT,
    hints TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create indexes for faster filtering and searching
CREATE INDEX IF NOT EXISTS idx_questions_difficulty
ON interview_questions(difficulty);

CREATE INDEX IF NOT EXISTS idx_questions_type
ON interview_questions(question_type);

CREATE INDEX IF NOT EXISTS idx_questions_company
ON interview_questions(company);

CREATE INDEX IF NOT EXISTS idx_questions_topics
ON interview_questions(topics);

CREATE INDEX IF NOT EXISTS idx_questions_category
ON interview_questions(category);

CREATE INDEX IF NOT EXISTS idx_questions_search
ON interview_questions USING gin(to_tsvector('english', question_text));

-- ========================================
-- PART 2: INSERT CODING QUESTIONS
-- ========================================

-- Easy Questions (7)
INSERT INTO interview_questions (question, difficulty, category, tags, constraints, examples, hints, source) VALUES
('Write a function to find two numbers in an array that sum to a target value', 'Easy', 'Coding', 'arrays,hash-table,two-pointers', 'Array length: 2 <= n <= 10^4; Values: -10^9 <= nums[i] <= 10^9; Exactly one solution exists', 'Input: nums = [2,7,11,15], target = 9; Output: [0,1]; Explanation: nums[0] + nums[1] = 2 + 7 = 9', 'Use a hash map to store numbers you''ve seen. For each number, check if target - number exists in the map.', 'Go Interview Practice - Challenge 1'),

('Reverse a string in-place without using built-in reverse functions', 'Easy', 'Coding', 'strings,two-pointers', '1 <= string length <= 10^5; String contains ASCII printable characters', 'Input: ''hello''; Output: ''olleh''', 'Use two pointers - one at start, one at end. Swap and move inward.', 'Go Interview Practice - Challenge 2'),

('Implement a function to count word frequency in a text file', 'Easy', 'Coding', 'hash-table,strings,file-processing', 'File size: up to 10MB; Words separated by spaces/punctuation', 'Input: ''hello world hello''; Output: {''hello'': 2, ''world'': 1}', 'Use a hash map. Normalize words (lowercase, remove punctuation).', 'Go Interview Practice - Challenge 6'),

('Convert temperature between Fahrenheit and Celsius', 'Easy', 'Coding', 'math,conversion', 'Temperature range: -273.15°C to 10^6°C', 'Input: 32°F; Output: 0°C; Formula: C = (F - 32) * 5/9', 'Remember the conversion formulas. Handle edge cases like absolute zero.', 'Go Interview Practice - Challenge 18'),

('Implement binary search on a sorted array', 'Easy', 'Coding', 'arrays,binary-search,divide-and-conquer', 'Array is sorted; 1 <= array length <= 10^6; -10^9 <= nums[i] <= 10^9', 'Input: nums = [1,3,5,7,9], target = 5; Output: 2', 'Divide array in half. Compare middle with target. Recurse on appropriate half.', 'Go Interview Practice - Challenge 21'),

('Solve the coin change problem using greedy algorithm', 'Easy', 'Coding', 'greedy,dynamic-programming,arrays', 'Coins: [1,5,10,25]; Amount: 0 <= n <= 10^4', 'Input: amount = 41; Output: [25,10,5,1] (4 coins)', 'Sort coins descending. Use largest coin possible repeatedly.', 'Go Interview Practice - Challenge 22'),

('Implement merge sort algorithm', 'Easy', 'Coding', 'sorting,divide-and-conquer,recursion', 'Array length: 0 <= n <= 10^5; Values: -10^9 <= nums[i] <= 10^9', 'Input: [38,27,43,3,9,82,10]; Output: [3,9,10,27,38,43,82]', 'Divide array in half recursively until size 1. Merge sorted halves.', 'Classic DSA');

-- Medium Questions (13)
INSERT INTO interview_questions (question, difficulty, category, tags, constraints, examples, hints, source) VALUES
('Implement concurrent graph BFS with goroutines', 'Medium', 'Coding', 'graphs,bfs,concurrency,channels', 'Graph nodes: 1 <= n <= 10^4; Edges: 0 <= edges <= n^2', 'Input: graph with 5 nodes; Output: BFS traversal order', 'Use channels for communication between goroutines. Synchronize access to visited set.', 'Go Interview Practice - Challenge 4'),

('Create HTTP authentication middleware', 'Medium', 'Coding', 'web,middleware,authentication,http', 'Handle JWT/Basic auth; Support custom auth logic', 'Request with token → validate → next() or 401', 'Check Authorization header. Validate token/credentials. Call next handler or return error.', 'Go Interview Practice - Challenge 5'),

('Implement a bank account system with error handling', 'Medium', 'Coding', 'oop,error-handling,concurrency', 'Support deposits, withdrawals, balance checks; Thread-safe operations', 'Account balance: $100; Withdraw $150 → Error: insufficient funds', 'Use mutex for thread safety. Validate operations before executing.', 'Go Interview Practice - Challenge 7'),

('Create a polymorphic shape calculator', 'Medium', 'Coding', 'oop,interfaces,polymorphism', 'Support Circle, Rectangle, Triangle; Calculate area and perimeter', 'Circle(r=5) → Area: 78.54, Perimeter: 31.42', 'Define interface with area() and perimeter() methods. Implement for each shape.', 'Go Interview Practice - Challenge 10'),

('Implement SQL database CRUD operations', 'Medium', 'Coding', 'database,sql,crud', 'Support SELECT, INSERT, UPDATE, DELETE; Handle SQL injection', 'Insert user → Read user → Update email → Delete user', 'Use prepared statements. Handle connection pooling. Validate inputs.', 'Go Interview Practice - Challenge 13'),

('Build a simple microservice with gRPC', 'Medium', 'Coding', 'grpc,microservices,protobuf', 'Define service in .proto; Implement server and client; Handle errors', 'Define Calculator service → Add(a, b) → Returns sum', 'Define protobuf schema. Generate code. Implement server logic. Create client.', 'Go Interview Practice - Challenge 14'),

('Optimize code for better performance', 'Medium', 'Coding', 'optimization,profiling,algorithms', 'Reduce time complexity; Memory optimization; Use appropriate data structures', 'O(n^2) → O(n log n) using better algorithm', 'Profile first. Identify bottlenecks. Use efficient data structures. Cache results.', 'Go Interview Practice - Challenge 16'),

('Implement circuit breaker pattern', 'Medium', 'Coding', 'design-patterns,resilience,fault-tolerance', 'States: Closed, Open, Half-Open; Failure threshold; Timeout', '3 failures → Open circuit → Wait 30s → Try again', 'Track failures. After threshold, open circuit. After timeout, allow one test request.', 'Go Interview Practice - Challenge 20'),

('Implement string pattern matching (KMP algorithm)', 'Medium', 'Coding', 'strings,pattern-matching,algorithms', 'Text length: 1 <= n <= 10^6; Pattern: 1 <= m <= n', 'Text: ''ababcababc'', Pattern: ''ababc'' → Found at index 0, 5', 'Build failure function. Use it to skip unnecessary comparisons.', 'Go Interview Practice - Challenge 23'),

('Implement generic data structures in Go', 'Medium', 'Coding', 'generics,data-structures,type-parameters', 'Support any comparable type; Implement Stack, Queue, BST', 'Stack[int] → Push(5) → Pop() → 5', 'Use type parameters. Define constraints. Implement common operations.', 'Go Interview Practice - Challenge 27'),

('Implement context management for cancellation', 'Medium', 'Coding', 'context,concurrency,cancellation', 'Handle timeouts, deadlines, cancellation; Propagate context', 'Context with 5s timeout → Long operation → Cancel after 5s', 'Use context.WithTimeout. Check ctx.Done() in loops. Return on cancellation.', 'Go Interview Practice - Challenge 30'),

('Find all pairs with given sum in array', 'Medium', 'Coding', 'arrays,hash-table,two-pointers', 'Array length: 1 <= n <= 10^4; May have duplicates', 'Input: [1,5,7,-1,5], sum = 6; Output: [(1,5), (7,-1), (1,5)]', 'Use hash set. For each num, check if (sum - num) exists.', 'Classic DSA'),

('Detect cycle in linked list', 'Medium', 'Coding', 'linked-list,two-pointers,cycle-detection', 'List length: 0 <= n <= 10^4; May contain cycle', 'Input: 1→2→3→4→2 (cycle); Output: true', 'Floyd''s algorithm: Use slow and fast pointers. If they meet, cycle exists.', 'Classic DSA');

-- Advanced Questions (10)
INSERT INTO interview_questions (question, difficulty, category, tags, constraints, examples, hints, source) VALUES
('Build a chat server using channels', 'Advanced', 'Coding', 'concurrency,channels,networking', 'Handle multiple clients; Broadcast messages; Client disconnect', 'Client A sends ''hello'' → All clients receive ''hello''', 'Central goroutine manages broadcast channel. Each client has send/receive channels.', 'Go Interview Practice - Challenge 8'),

('Create RESTful API for book management', 'Advanced', 'Coding', 'rest-api,http,crud,json', 'GET /books, POST /book, PUT /book/:id, DELETE /book/:id', 'POST /book {title: ''Go Programming''} → 201 Created', 'Define routes. Parse JSON. Validate input. Store in database. Return JSON responses.', 'Go Interview Practice - Challenge 9'),

('Build concurrent web content aggregator', 'Advanced', 'Coding', 'concurrency,http,goroutines,sync', 'Fetch multiple URLs concurrently; Aggregate results; Handle errors', 'Fetch 10 URLs → Aggregate content → Return combined result', 'Use sync.WaitGroup. Launch goroutines for each URL. Collect results with mutex.', 'Go Interview Practice - Challenge 11'),

('Create file processing pipeline', 'Advanced', 'Coding', 'concurrency,pipelines,channels', 'Read → Transform → Write; Handle large files; Memory efficient', 'Read CSV → Filter rows → Transform data → Write JSON', 'Use pipeline pattern. Channel for each stage. Process chunks, not entire file.', 'Go Interview Practice - Challenge 12'),

('Implement OAuth2 authentication flow', 'Advanced', 'Coding', 'oauth,authentication,security,jwt', 'Support authorization code flow; Token refresh; Secure storage', 'User login → Redirect to OAuth → Exchange code for token', 'Implement authorization endpoint, token endpoint, refresh logic. Validate tokens.', 'Go Interview Practice - Challenge 15'),

('Solve longest increasing subsequence (DP)', 'Advanced', 'Coding', 'dynamic-programming,arrays,algorithms', 'Array length: 1 <= n <= 2500; Values: -10^4 <= nums[i] <= 10^4', 'Input: [10,9,2,5,3,7,101,18]; Output: 4 (LIS: [2,3,7,101])', 'Use DP array where dp[i] = length of LIS ending at i. For each i, check all j < i.', 'Go Interview Practice - Challenge 24'),

('Implement shortest path algorithm (Dijkstra)', 'Advanced', 'Coding', 'graphs,shortest-path,algorithms,priority-queue', 'Graph nodes: 1 <= n <= 1000; Non-negative weights', 'Graph: A-B(1), A-C(4), B-C(2); Shortest path A→C: 3 (A→B→C)', 'Use priority queue. Track distances. Update distances when shorter path found.', 'Go Interview Practice - Challenge 25'),

('Build regex text processor', 'Advanced', 'Coding', 'regex,strings,parsing', 'Support pattern matching, replacement, extraction; Handle edge cases', 'Text: ''Email: user@example.com''; Extract: ''user@example.com''', 'Compile regex patterns. Use capture groups. Handle multiple matches.', 'Go Interview Practice - Challenge 26'),

('Implement cache with eviction policies', 'Advanced', 'Coding', 'cache,lru,lfu,data-structures', 'Support LRU, LFU, FIFO; Fixed capacity; O(1) operations', 'LRU cache size 3: Put(1,1), Put(2,2), Put(3,3), Put(4,4) → Evicts 1', 'LRU: HashMap + Doubly Linked List. LFU: HashMap + Min Heap + Frequency map.', 'Go Interview Practice - Challenge 28'),

('Implement rate limiter', 'Advanced', 'Coding', 'rate-limiting,concurrency,algorithms', 'Support token bucket, sliding window; Thread-safe; Configurable limits', '10 requests/sec limit: 11th request in same second → Reject', 'Token bucket: Refill tokens at rate. Sliding window: Track timestamps in queue.', 'Go Interview Practice - Challenge 29');

-- ========================================
-- PART 3: VERIFY SETUP
-- ========================================

-- Show table counts
SELECT 'Tables Created' as status;

SELECT
    'interview_questions' as table_name,
    difficulty,
    COUNT(*) as count
FROM interview_questions
WHERE category = 'Coding'
GROUP BY difficulty
ORDER BY difficulty;
