<?php
/**
 * Stitch functions and definitions
 *
 * @package Stitch
 * @since Stitch 1.0
 */

/**
 * Set the content width based on the theme's design and stylesheet.
 *
 * @since Stitch 1.0
 */
if ( ! isset( $content_width ) )
	$content_width = 580; /* pixels */

if ( ! function_exists( 'stitch_setup' ) ) :
/**
 * Sets up theme defaults and registers support for various WordPress features.
 *
 * Note that this function is hooked into the after_setup_theme hook, which runs
 * before the init hook. The init hook is too late for some features, such as indicating
 * support post thumbnails.
 *
 * @since Stitch 1.0
 */
function stitch_setup() {

	/**
	 * Custom template tags for this theme.
	 */
	require( get_template_directory() . '/inc/template-tags.php' );

	/**
	 * Custom functions that act independently of the theme templates
	 */
	require( get_template_directory() . '/inc/extras.php' );

	/**
	 * Custom Theme Options
	 */
	require( get_template_directory() . '/inc/customizer.php' );

	/* Jetpack Infinite Scroll */
	add_theme_support( 'infinite-scroll', array(
		'container'  => 'content',
		'footer'     => 'page',
	) );

	/**
	 * Make theme available for translation
	 * Translations can be filed in the /languages/ directory
	 * If you're building a theme based on Stitch, use a find and replace
	 * to change 'stitch' to the name of your theme in all the template files
	 */
	load_theme_textdomain( 'stitch', get_template_directory() . '/languages' );

	/**
	 * Add default posts and comments RSS feed links to head
	 */
	add_theme_support( 'automatic-feed-links' );

	/**
	 * Add support for custom backgrounds
	 */
	$stitch_defaults = array(
		'default-color'          => 'f7f6f2',
		'default-image'          => get_template_directory_uri() . '/images/background2.jpg',
	);
	add_theme_support( 'custom-background', $stitch_defaults );

	/**
	 * This theme uses wp_nav_menu() in one location.
	 */
	register_nav_menus( array(
		'primary' => __( 'Primary Menu', 'stitch' ),
	) );

	/**
	 * Add support for the Aside Post Formats
	 */
	add_theme_support( 'post-formats', array( 'aside', 'image', 'video', 'quote', 'link', 'status' ) );
}
endif; // stitch_setup
add_action( 'after_setup_theme', 'stitch_setup' );

/* Filter to add author credit to Infinite Scroll footer */
function stitch_footer_credits( $credit ) {
	$credit = sprintf( __( '%3$s | Theme: %1$s by %2$s.', 'stitch' ), 'Stitch', '<a href="http://carolinemoore.net/" rel="designer">Caroline Moore</a>', '<a href="http://wordpress.org/" title="' . esc_attr( __( 'A Semantic Personal Publishing Platform', 'stitch' ) ) . '" rel="generator">Proudly powered by WordPress</a>' );
	return $credit;
}
add_filter( 'infinite_scroll_credit', 'stitch_footer_credits' );

/**
 * Register widgetized area and update sidebar with default widgets
 *
 * @since Stitch 1.0
 */
function stitch_widgets_init() {
	register_sidebar( array(
		'name' => __( 'Sidebar', 'stitch' ),
		'id' => 'sidebar-1',
		'before_widget' => '<aside id="%1$s" class="widget %2$s">',
		'after_widget' => '</aside>',
		'before_title' => '<h1 class="widget-title">',
		'after_title' => '</h1>',
	) );
}
add_action( 'widgets_init', 'stitch_widgets_init' );

/**
 * Enqueue scripts and styles
 */
function stitch_scripts() {
	wp_enqueue_style( 'style', get_stylesheet_uri() );

	wp_enqueue_style( 'stitch_fjalla' );
	wp_enqueue_style( 'stitch_rufina' );
	wp_enqueue_style( 'stitch_pacifico' );

	wp_enqueue_script( 'small-menu', get_template_directory_uri() . '/js/small-menu.js', array( 'jquery' ), '20120206', true );

	if ( is_singular() && comments_open() && get_option( 'thread_comments' ) ) {
		wp_enqueue_script( 'comment-reply' );
	}

	if ( is_singular() && wp_attachment_is_image() ) {
		wp_enqueue_script( 'keyboard-image-navigation', get_template_directory_uri() . '/js/keyboard-image-navigation.js', array( 'jquery' ), '20120202' );
	}
}
add_action( 'wp_enqueue_scripts', 'stitch_scripts' );

function stitch_header_position() {

	if ( 'true' != get_theme_mod( 'header_position', 'true' ) )
		return;
?>
<style type="text/css">
	#masthead {
		position: fixed;
	}
	@media screen and ( max-width: 800px ) {
		#masthead {
			position: relative;
		}
	}
</style>

<?php
}
add_action( 'wp_head', 'stitch_header_position' );

/**
 * Enqueue Google Fonts
 */
function stitch_fonts() {

	$protocol = is_ssl() ? 'https' : 'http';

	/*	translators: If there are characters in your language that are not supported
		by Pacifico, translate this to 'off'. Do not translate into your own language. */

	if ( 'off' !== _x( 'on', 'Pacifico font: on or off', 'stitch' ) ) {

		wp_register_style( 'stitch_pacifico', "$protocol://fonts.googleapis.com/css?family=Pacifico&subset=latin,latin-ext" );

	}

	/*	translators: If there are characters in your language that are not supported
		by Fjalla One, translate this to 'off'. Do not translate into your own language. */

	if ( 'off' !== _x( 'on', 'Fjalla One font: on or off', 'stitch' ) ) {

		wp_register_style( 'stitch_fjalla', "$protocol://fonts.googleapis.com/css?family=Fjalla+One&subset=latin,latin-ext" );

	}

	/*	translators: If there are characters in your language that are not supported
		by Rufina, translate this to 'off'. Do not translate into your own language. */

	if ( 'off' !== _x( 'on', 'Rufina font: on or off', 'stitch' ) ) {

		wp_register_style( 'stitch_rufina', "$protocol://fonts.googleapis.com/css?family=Rufina:400,700" );

	}

}
add_action( 'init', 'stitch_fonts' );


/**
 * Enqueue Google Fonts for custom headers
 */
function stitch_admin_scripts( $hook_suffix ) {

	if ( 'appearance_page_custom-header' != $hook_suffix )
		return;

	wp_enqueue_style( 'stitch_fjalla' );
	wp_enqueue_style( 'stitch_rufina' );
	wp_enqueue_style( 'stitch_pacifico' );

}
add_action( 'admin_enqueue_scripts', 'stitch_admin_scripts' );

/**
 * Implement the Custom Header feature
 */
require( get_template_directory() . '/inc/custom-header.php' );
