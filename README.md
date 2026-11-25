<h1>Wishlist Bot✨</h1>

<h3>Description</h3>
<p>This bot was created so that everyone can leave their gift wishes in it and share them with their friends!</p>
<p>What distinguishes it from analogs is that the bot works entirely through messages in the messenger itself, without using a mini-app, which makes it easier to use.</p>

<h3>Features</h3>
<ul>
  <li>Create and view your own wishlist of gifts</li>
  <li>View a friend's wishlist by username</li>
  <li>Add new gifts (text + image)</li>
  <li>Delete gifts from your wishlist</li>
  <li>Close your wishlist with a code word (for privacy)</li>
  <li>Works entirely through regular messages in Telegram (without mini-app)</li>
</ul>

<h3>Video Demo</h3>
<p>Watch the bot interface and in action:</p>
<img src="for_readme/video1.gif" width="600">
<img src="for_readme/video2.gif" width="600">

<h3>How it works</h3>
<p>To understand how the bot works, I created something like an activity diagram.</p>

<img src="for_readme/diagram.png" width="800">

<p>The diagram above illustrates the bot's primary operational scenarios. It shows how the bot handles user actions, such as viewing wishlists (using <code>ShowFriendList_handler.py</code> for friends' wishlists and <code>ShowMyList_handler.py</code> for one's own), creating gifts (<code>CreateNewGift_handler.py</code>), securing wishlists with a code word (<code>CloseMyList_handler.py</code>), and deleting gifts (<code>DeleteMyGift_handler.py</code>).</p>

<p>It is also worth noting the files <code>db.py</code> and <code>wishlist_view.py</code>.</p>

<p><code>wishlist_view.py</code> contains the logic for retrieving a wishlist and formatting it into messages. It is used by <code>ShowFriendList_handler.py</code>, <code>ShowMyList_handler.py</code>, and <code>DeleteMyGift_handler.py</code>.</p>

<p><code>db.py</code> contains the database connection settings and a function for registering users in the <code>users</code> table.</p>

<h3>Environment requirements</h3>
<table>
  <tr>
    <td><b>Python</b></td>
    <td>v3.13</td>
  </tr>
  <tr>
    <td><b>Database</b></td>
    <td>PostgreSQL v18.6</td>
  </tr>
  <tr>
    <td><b>Python libraries</b></td>
    <td><code>python-telegram-bot==22.5</code>, <code>psycopg2</code></td>
  </tr>
  <tr>
    <td><b>Telegram</b></td>
    <td>Bot Token from @BotFather</td>
  </tr>
  <tr>
    <td><b>Database access</b></td>
    <td>Access to a PostgreSQL instance (database name, user, password, host, port)</td>
  </tr>
</table>

<h3>Database Setup</h3>
<p>The following SQL script creates the tables required by the bot:</p>
<pre><code class="language-sql">CREATE TABLE users
(
    user_id BIGINT PRIMARY KEY,
    username VARCHAR(32) UNIQUE, 
    wishlist_code VARCHAR(64)
);

CREATE TABLE gifts
(
    id SERIAL PRIMARY KEY,
    user_id  BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    label TEXT NOT NULL,
    image_file_id VARCHAR(255),
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_gifts_user_id ON gifts(user_id);</code></pre>

<h3>Installation</h3>
<ol>
  <li>Clone the repository:
    <pre><code>git clone https://github.com/Dunwitch666/Wish-list-telegram-bot.git</code></pre>
    <pre><code>cd Wish-list-telegram-bot</code></pre>
  </li>
  <li>Install Python 3.13.</li>
  <li>Install dependencies:
    <pre><code>pip install python-telegram-bot psycopg2-binary python-dotenv</code></pre>
  </li>
  <li>Set up PostgreSQL and create a database for the bot.</li>
  <li>Configure environment variables in the .env document: bot token (<code>BOT_TOKEN</code>) and database connection parameters.</li>
  <li>Run the bot:
    <pre><code>python main.py</code></pre>
  </li>
</ol>

<h3>Stack</h3>
<ul>
  <li>python v3.13</li>
  <li>python-telegram-bot v22.5</li>
  <li>postgreSQL v18.6</li>
  <li>psycopg2</li>
</ul>