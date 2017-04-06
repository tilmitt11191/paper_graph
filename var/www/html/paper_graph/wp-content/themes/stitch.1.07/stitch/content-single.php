<?php
/**
 * @package Stitch
 * @since Stitch 1.0
 */
?>

<article id="post-<?php the_ID(); ?>" <?php post_class(); ?>>
	<header class="entry-header">
		<?php the_title( '<h1 class="entry-title">', '</h1>' ); ?>
		<?php edit_post_link( __( 'Edit', 'stitch' ), '<span class="edit-link">', '</span>' ); ?>
	</header><!-- .entry-header -->

	<div class="entry-content">
		<?php the_content(); ?>
		<?php wp_link_pages( array( 'before' => '<div class="page-links">' . __( 'Pages:', 'stitch' ), 'after' => '</div>' ) ); ?>
	</div><!-- .entry-content -->

	<footer class="entry-meta">
		<?php stitch_posted_on(); ?>
		<span class="sep"></span>
		<?php
			/* translators: used between list items, there is a space after the comma */
			$category_list = get_the_category_list( __( ', ', 'stitch' ) );

			/* translators: used between list items, there is a space after the comma */
			$tag_list = get_the_tag_list( '', __( ', ', 'stitch' ) );

			if ( ! stitch_categorized_blog() ) {
				// This blog only has 1 category so we just need to worry about tags in the meta text
				if ( '' != $tag_list ) {
					$meta_text = __( 'Tagged %2$s<span class="sep"></span><a href="%3$s" title="Permalink to %4$s" rel="bookmark">Permalink</a>', 'stitch' );
				} else {
					$meta_text = __( '<a href="%3$s" title="Permalink to %4$s" rel="bookmark">Permalink</a>', 'stitch' );
				}

			} else {
				// But this blog has loads of categories so we should probably display them here
				if ( '' != $tag_list ) {
					$meta_text = __( 'Posted in %1$s<span class="sep"></span>Tagged %2$s<span class="sep"></span><a href="%3$s" title="Permalink to %4$s" rel="bookmark">Permalink</a>', 'stitch' );
				} else {
					$meta_text = __( 'Posted in %1$s<span class="sep"></span><a href="%3$s" title="Permalink to %4$s" rel="bookmark">Permalink</a>', 'stitch' );
				}

			} // end check for categories on this blog

			printf(
				$meta_text,
				$category_list,
				$tag_list,
				get_permalink(),
				the_title_attribute( 'echo=0' )
			);
		?>

	</footer><!-- .entry-meta -->
</article><!-- #post-<?php the_ID(); ?> -->
