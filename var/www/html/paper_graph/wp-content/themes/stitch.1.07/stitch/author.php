<?php
/**
 * The template for displaying Author Archive pages.
 *
 * Learn more: http://codex.wordpress.org/Template_Hierarchy
 *
 * @package Stitch
 * @since Stitch 1.0
 */

get_header(); ?>

		<section id="primary" class="site-content">
			<div id="content" role="main">

			<?php if ( have_posts() ) : ?>

				<header class="page-header">
					<h1 class="page-title"><?php _e( 'Author Archives', 'stitch' ); ?></h1>
					<div class="author-archives-header">
						<?php
								/* Queue the first post, that way we know
								 * what author we're dealing with (if that is the case).
								*/
								the_post();
								printf( '<span class="author-archives-img">%1$s</span>', get_avatar( get_the_author_meta( 'ID' ), '100' ) );
								print( '<div class="author-info">' );
								printf( '<span class="author-archives-name">' . __( '%s', 'stitch' ) . '</span>', '<span class="vcard"><a class="url fn n" href="' . get_author_posts_url( get_the_author_meta( "ID" ) ) . '" title="' . esc_attr( get_the_author() ) . '" rel="me">' . get_the_author() . '</a></span>' );
								printf( '<span class="author-archives-url">' . __( '%s', 'stitch' ) . '</span>', '<a href="' . get_the_author_meta( 'user_url', get_the_author_meta( 'ID' ) ) . '" title="' . esc_attr( get_the_author() . '\'s website' ) . '">' . get_the_author_meta( 'user_url', get_the_author_meta( 'ID' ) ) . '</a>' );
								printf( '<span class="author-archives-bio">' . __( '%s', 'stitch' ) . '</span>', get_the_author_meta( 'user_description', get_the_author_meta( 'ID' ) ) );
								print( '</div>' );
						?>
					</div>

				<?php rewind_posts(); ?>

				<?php /* Start the Loop */ ?>
				<?php while ( have_posts() ) : the_post(); ?>

					<?php
						/* Include the Post-Format-specific template for the content.
						 * If you want to overload this in a child theme then include a file
						 * called content-___.php (where ___ is the Post Format name) and that will be used instead.
						 */
						get_template_part( 'content', get_post_format() );
					?>

				<?php endwhile; ?>

				<?php stitch_content_nav( 'nav-below' ); ?>

			<?php else : ?>

				<?php get_template_part( 'no-results', 'archive' ); ?>

			<?php endif; ?>

			</div><!-- #content -->
		</section><!-- #primary .site-content -->

<?php get_footer(); ?>