<?php
/**
 * WordPress の基本設定
 *
 * このファイルは、インストール時に wp-config.php 作成ウィザードが利用します。
 * ウィザードを介さずにこのファイルを "wp-config.php" という名前でコピーして
 * 直接編集して値を入力してもかまいません。
 *
 * このファイルは、以下の設定を含みます。
 *
 * * MySQL 設定
 * * 秘密鍵
 * * データベーステーブル接頭辞
 * * ABSPATH
 *
 * @link http://wpdocs.osdn.jp/wp-config.php_%E3%81%AE%E7%B7%A8%E9%9B%86
 *
 * @package WordPress
 */

// 注意:
// Windows の "メモ帳" でこのファイルを編集しないでください !
// 問題なく使えるテキストエディタ
// (http://wpdocs.osdn.jp/%E7%94%A8%E8%AA%9E%E9%9B%86#.E3.83.86.E3.82.AD.E3.82.B9.E3.83.88.E3.82.A8.E3.83.87.E3.82.A3.E3.82.BF 参照)
// を使用し、必ず UTF-8 の BOM なし (UTF-8N) で保存してください。

// ** MySQL 設定 - この情報はホスティング先から入手してください。 ** //
/** WordPress のためのデータベース名 */
define('DB_NAME', 'paper_graph');

/** MySQL データベースのユーザー名 */
define('DB_USER', 'paper_graph');

/** MySQL データベースのパスワード */
define('DB_PASSWORD', 'pg');

/** MySQL のホスト名 */
define('DB_HOST', 'localhost');

/** データベースのテーブルを作成する際のデータベースの文字セット */
define('DB_CHARSET', 'utf8mb4');

/** データベースの照合順序 (ほとんどの場合変更する必要はありません) */
define('DB_COLLATE', '');

/**#@+
 * 認証用ユニークキー
 *
 * それぞれを異なるユニーク (一意) な文字列に変更してください。
 * {@link https://api.wordpress.org/secret-key/1.1/salt/ WordPress.org の秘密鍵サービス} で自動生成することもできます。
 * 後でいつでも変更して、既存のすべての cookie を無効にできます。これにより、すべてのユーザーを強制的に再ログインさせることになります。
 *
 * @since 2.6.0
 */
define('AUTH_KEY',         'VrGk.cBWqN~2MXsh pk8P]v;?ObL/= ws4`xY]c# iPtF=nH4VR^>OXE0J}21n7s');
define('SECURE_AUTH_KEY',  'UFJ[5PUY/HBFLbT~_iPFhO|*e[eeXqWB[kMy%Rd7sqO;VRc6JJW5#hmgC2Vbx]9j');
define('LOGGED_IN_KEY',    'Z8:0$IW5qo~l]Y/iN0K/,mKirL7&H#dPD!W<xQJGy!{/ CSn|iCx:*/;H6;]/6vc');
define('NONCE_KEY',        ',#<d0?G`xo$$Jt8zROwqscL*;SM)Lsc]<zN0<l?b0WBEw^Jk4_Hz<;LnRG;7okqO');
define('AUTH_SALT',        'GD#8ve9sxvh`6],9)-w{qWzxGig6&>|rDK%kJBYA|Ke|H$YM#sE-2/a]o-(Y>fij');
define('SECURE_AUTH_SALT', 'm+VWDPYiBltH9<j/}?GMBY]m29e3;UTE][WkkKdsNOGa[:l8V|[ m@WpxR31E6i$');
define('LOGGED_IN_SALT',   '} gCe!Meo?)v4X|t[geh|QZA9frQ|u0UR3zl.*rQl,6>,OO5mtlV/-<|,:v`c*j_');
define('NONCE_SALT',       ':5/9TCA-s~~</-%F^0%mSdv_[cH*shvgl<I6auN>y8m~_ jpG>V-cy8o(B,w[}he');

/**#@-*/

/**
 * WordPress データベーステーブルの接頭辞
 *
 * それぞれにユニーク (一意) な接頭辞を与えることで一つのデータベースに複数の WordPress を
 * インストールすることができます。半角英数字と下線のみを使用してください。
 */
$table_prefix  = 'pg_';

/**
 * 開発者へ: WordPress デバッグモード
 *
 * この値を true にすると、開発中に注意 (notice) を表示します。
 * テーマおよびプラグインの開発者には、その開発環境においてこの WP_DEBUG を使用することを強く推奨します。
 *
 * その他のデバッグに利用できる定数については Codex をご覧ください。
 *
 * @link http://wpdocs.osdn.jp/WordPress%E3%81%A7%E3%81%AE%E3%83%87%E3%83%90%E3%83%83%E3%82%B0
 */
define('WP_DEBUG', false);

/* 編集が必要なのはここまでです ! WordPress でブログをお楽しみください。 */

/** Absolute path to the WordPress directory. */
if ( !defined('ABSPATH') )
	define('ABSPATH', dirname(__FILE__) . '/');

/** Sets up WordPress vars and included files. */
require_once(ABSPATH . 'wp-settings.php');
